import subprocess

from urllib3.connectionpool import HTTPConnectionPool


def apply_tc():
    subprocess.run(["python", "scripts/manage_tc.py", "apply"], check=True)

def remove_tc():
    subprocess.run(["python", "scripts/manage_tc.py", "remove"], check=True)


class PatchedMakeRequest:
    original_make_request = HTTPConnectionPool._make_request

    def __enter__(self):
        """
        Apply patch as long as the context manager is alive
        """
        self.patch_make_request()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Removing patch from HTTPConnectionPool._make_request
        """
        HTTPConnectionPool._make_request = PatchedMakeRequest.original_make_request
        return False

    def patch_make_request(self) -> None:
        """
        Since setting a retry configuration for the requests package relies on the urllib3 package,
        I couldn't find any other way of interrupting the network traffic other than monkey-patching this method.
        """
        def patched_make_request(self, conn, method, url, **kwargs):
            """
            In this method, self refers to HTTPConnectionPool, not PatchedMakeRequest
            """
            if not hasattr(self, 'tc_applied'):
                # First time, applying tc!
                apply_tc()
                self.tc_applied = True
            else:
                # Not first time, removing tc!
                remove_tc()
                del self.tc_applied
            
            response = PatchedMakeRequest.original_make_request(self, conn, method, url, **kwargs)
            return response

        # Patching HTTPConnectionPool._make_request
        HTTPConnectionPool._make_request = patched_make_request  # type: ignore



        