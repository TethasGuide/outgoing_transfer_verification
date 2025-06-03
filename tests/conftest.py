import sys
from types import ModuleType

# Provide a minimal stub for the requests package if it is not installed
if 'requests' not in sys.modules:
    requests_stub = ModuleType('requests')

    def dummy_get(*args, **kwargs):
        raise RuntimeError('requests.get should be mocked in tests')

    requests_stub.get = dummy_get

    class DummySession:
        def get(self, *args, **kwargs):
            raise RuntimeError('session.get should be mocked in tests')

        def close(self):
            pass

    requests_stub.Session = DummySession
    sys.modules['requests'] = requests_stub

# Stub out office365 modules if not installed so imports succeed
if 'office365' not in sys.modules:
    office365 = ModuleType('office365')
    runtime = ModuleType('runtime')
    auth_mod = ModuleType('auth')
    user_cred_mod = ModuleType('user_credential')
    user_cred_mod.UserCredential = type('UserCredential', (), {})
    auth_mod.user_credential = user_cred_mod
    runtime.auth = auth_mod
    sharepoint_mod = ModuleType('sharepoint')
    client_ctx_mod = ModuleType('client_context')
    client_ctx_mod.ClientContext = type('ClientContext', (), {})
    sharepoint_mod.client_context = client_ctx_mod
    office365.runtime = runtime
    office365.sharepoint = sharepoint_mod
    sys.modules['office365'] = office365
    sys.modules['office365.runtime'] = runtime
    sys.modules['office365.runtime.auth'] = auth_mod
    sys.modules['office365.runtime.auth.user_credential'] = user_cred_mod
    sys.modules['office365.sharepoint'] = sharepoint_mod
    sys.modules['office365.sharepoint.client_context'] = client_ctx_mod
