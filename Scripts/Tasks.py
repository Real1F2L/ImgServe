import asyncio, os
#
from pathlib import Path
from datetime import datetime, timedelta, time
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
            await asyncio.to_thread(
                self._clear_cache,
                ServerData.get_cache_path(),
                keep_cache_for_hours,
            )

        except PermissionError:
            print(f"Failed to clear cache in {ServerData.get_cache_path()} due insufficient permissions to delete files in this folder.")

        except Exception as e:
            print(f"Failed to clear cache: {e}")

    @staticmethod
    def _clear_cache(cache_path: Path, keep_cache_for_hours: int):
        # Loop over all files in the cache
        for root, dirs, files in os.walk(cache_path, topdown=False):
            for file in files:
                path = Path(root) / file

                # If the file is not a resizable image, delete it
                if path.suffix.lstrip(".") not in utils.supported_resize_image_extensions:
                    path.unlink()
                    continue

                # If the file is older than the keep_cache_for_hours, delete it
                if (
                    keep_cache_for_hours != -1 and
                    datetime.now() - datetime.fromtimestamp(path.stat().st_mtime) > timedelta(hours=keep_cache_for_hours)
                ):
                    path.unlink()

            # Delete empty directories
            for directory in dirs:
                path = Path(root) / directory
                if path.is_dir() and not any(path.iterdir()):
                    path.rmdir()



class PurgeCacheTask(ScheduledTask):
    """Clears all cache in the cache folder"""

    async def execute(self):
        self.last_execution = datetime.now()
        print("Purging Cache...")

        try:
            await asyncio.to_thread(self._purge_cache, ServerData.get_cache_path())
            print(f"{Color.g}Successfully purged cache.{Color.re}")

        
        except PermissionError:
            print(f"{Color.r}Failed to purge cache in {ServerData.get_cache_path()} due insufficient permissions to delete files in this folder.{Color.re}")

        except Exception as e:
            print(f"{Color.r}Failed to purge cache: {e}{Color.re}")

    @staticmethod
    def _purge_cache(cache_path: Path):
        # Loop over all files in the cache
        for root, dirs, files in os.walk(cache_path, topdown=False):
            # Delete all files first
            for file in files:
                (Path(root) / file).unlink()

            # Delete all directories (which should be empty now)
            for directory in dirs:
                (Path(root) / directory).rmdir()