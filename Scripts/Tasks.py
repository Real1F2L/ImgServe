import asyncio, os
#
from pathlib import Path
from datetime import datetime, timedelta, time
from dataclasses import dataclass
from Scripts.utils import Color
from Scripts import utils
from Scripts.ServerData import ServerData

class ScheduledExecute:
    def __init__(self, execute_time: time):
        self.execute_time = execute_time

        self.next_execution_time = datetime.combine(datetime.now().date() + timedelta(days=1), self.execute_time)

    def update_next_execution_time(self):
        """Sets the next execution time to tomorrow at the scheduled time"""
        self.next_execution_time = datetime.combine(datetime.now().date() + timedelta(days=1), self.execute_time)


class ScheduledTask:
    def __init__(self, name: str, execute_every_hours: int = -1, scheduled_executes: list[ScheduledExecute] = [], execute_now: bool = False):
        self.name = name
        self.task_started = True
        self.execute_now = execute_now

        # Execution
        self.last_execution = datetime.now()
        self.execute_every_hours = execute_every_hours
        self.scheduled_executes: list[ScheduledExecute] = scheduled_executes

    async def start_task(self):
        """Periodically checks if it is time to execute the task"""

        if self.execute_now:
            print(f"Scheduled task {self.name} is set to execute now.")
            await self.execute()

        while self.task_started:
            now = datetime.now()

            # If hourly checks are enabled
            if self.execute_every_hours != -1:

                # If it is past the execute time
                if now - self.last_execution > timedelta(hours=self.execute_every_hours):
                    await self.execute()

            # Check if its time for a scheduled execution
            for se in self.scheduled_executes[:]:
                # Execution date has passed
                if se.next_execution_time < now:
                    se.update_next_execution_time()
                    await self.execute()

            await asyncio.sleep(60) #? Wait second between checks

    def stop_task(self):
        self.task_started = False

    async def execute(self):
        self.last_execution = datetime.now()
        print(f"Execution of task {self.name} failed because it is not implemented.")
        raise NotImplementedError



class ClearCacheTask(ScheduledTask):
    """Clears cache in the cache folder"""

    async def execute(self):
        self.last_execution = datetime.now()
        print("Clearing Cache...")

        try:
            keep_cache_for_hours = int(ServerData.getData("keep_cache_for_hours"))
    
            # Check all dirs inside the cache folder
            for root, dirs, files in os.walk(ServerData.get_cache_path()):
    
                # Check files
                for file in files:
                    path = Path(root) / file

                    # Delete the file if it isn't a supported image
                    if not path.suffix.replace(".", "") in utils.supported_resize_image_extensions:
                        path.unlink()
                        continue

                    # Delete if it is older than cache date
                    if datetime.now() - path.stat().st_ctime > timedelta(hours=keep_cache_for_hours):
                        path.unlink()

                # Delete empty folders
                for dir in dirs:
                    path = Path(root) / dir
                    if len(os.listdir(path)) == 0:
                        path.rmdir()

        except PermissionError:
            print(f"Failed to clear cache in {ServerData.get_cache_path()} due insufficient permissions to delete files in this folder.")

        except Exception as e:
            print(f"Failed to clear cache: {e}")



class PurgeCacheTask(ScheduledTask):
    """Clears all cache in the cache folder"""

    async def execute(self):
        self.last_execution = datetime.now()
        print("Purging Cache...")

        try:
            # Delete all files and folders in the cache folder
            for root, dirs, files in os.walk(ServerData.get_cache_path(), topdown=False):
                for file in files:
                    (Path(root) / file).unlink()

                for directory in dirs:
                    (Path(root) / directory).rmdir()

        
        except PermissionError:
            print(f"{Color.r}Failed to purge cache in {ServerData.get_cache_path()} due insufficient permissions to delete files in this folder.{Color.re}")

        except Exception as e:
            print(f"{Color.r}Failed to purge cache: {e}{Color.re}")