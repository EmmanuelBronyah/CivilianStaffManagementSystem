from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.exceptions import Throttled
import time


class CustomAnonRateThrottle(AnonRateThrottle):
    scope = "custom_anon"
    rate = "3/minute"

    def allow_request(self, request, view):
        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        data = self.cache.get(self.key, {"attempts": [], "locked_until": 0})
        now = time.time()

        if data.get("locked_until", 0) > now:
            wait = int(data["locked_until"] - now)
            self.wait = wait
            raise Throttled(
                detail=f"You have exceeded the maximum attempts. Try again in {self.wait} seconds.",
            )

        attempts = [t for t in data["attempts"] if t > now - 60]

        if len(attempts) >= 3:
            lockout_until = now + 180
            self.cache.set(
                self.key, {"attempts": attempts, "locked_until": lockout_until}, 180
            )
            self.wait = 180
            raise Throttled(
                detail=f"You have exceeded the maximum attempts. Try again in {self.wait} seconds.",
            )

        attempts.append(now)
        self.cache.set(self.key, {"attempts": attempts, "locked_until": 0}, 180)
        return True


class CustomUserRateThrottle(UserRateThrottle):
    scope = "custom_user"
    rate = "6/minute"

    def allow_request(self, request, view):
        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        data = self.cache.get(self.key, {"attempts": [], "locked_until": 0})
        now = time.time()

        if data.get("locked_until", 0) > now:
            wait = int(data["locked_until"] - now)
            self.wait = wait
            raise Throttled(
                detail=f"You have exceeded the maximum attempts. Try again in {self.wait} seconds.",
            )

        attempts = [t for t in data["attempts"] if t > now - 60]

        if len(attempts) >= 3:
            lockout_until = now + 180
            self.cache.set(
                self.key, {"attempts": attempts, "locked_until": lockout_until}, 180
            )
            self.wait = 180
            raise Throttled(
                detail=f"You have exceeded the maximum attempts. Try again in {self.wait} seconds.",
            )

        attempts.append(now)
        self.cache.set(self.key, {"attempts": attempts, "locked_until": 0}, 180)
        return True
