from django_cron import CronJobBase, Schedule
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from events.models import EventWorker, Event
from contacts.models import Speaker, Organisation


import facebook

import logging
logger = logging.getLogger(__name__)

class FB(CronJobBase):
    RUN_EVERY_MINS = 120 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'events.tasks.FB'    # a unique code

    def do(self):
        logger.debug("cron job starting for: FB")

        #get the event worker for heltech
        try:
            ew = EventWorker.objects.get(page_name = "HEL Tech") #assume one worker for hel tech
            
        except ObjectDoesNotExist:
            logger.error("No event workers configured, cannot check events!")
            return
        except MultipleObjectsReturned:
            logger.error("Multiple workers found, do not know which one to run yet!")
            return
        
        graph = facebook.GraphAPI(access_token=ew.page_token, version="2.1")

        #get the page events
        
        fb_events = graph.get_connections(id=ew.page_id, connection_name="events")
        logger.debug("All events fetched, result:", str(fb_events))
        
        db_events = Event.objects.all()

        # any new events?
        for event in fb_events['data']:
            try:
                e = Event.objects.get(eid=str(event['id']))
                
                #exists, lets update the participant count
                ac = graph.get_object(id=event['id'], fields='attending_count')
                e.attending_count = ac['attending_count']
                e.save()
                    
            except ObjectDoesNotExist:
                # an uncached event, parse, and save
                ep = EventParser(event)
                ep.parse()
                e = Event( eid=ep.eid,
                           title=ep.title,
                           start_time=ep.start_time,
                           end_time=ep.end_time,
                           programme=ep.programme,
                           description=ep.description )
          
                e.save()
