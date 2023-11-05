from traffix_sdk.models.api_key import (
    TraffixAPIKey,
    TraffixAPIKeyCreate,
    TraffixAPIKeyRead,
    TraffixAPIKeyUpdate,
)
from traffix_sdk.models.category import (
    TraffixCategory,
    TraffixCategoryCreate,
    TraffixCategoryRead,
    TraffixCategoryUpdate,
)
from traffix_sdk.models.release import (
    TraffixRelease,
    TraffixReleaseCreate,
    TraffixReleaseRead,
    TraffixReleaseUpdate,
)
from traffix_sdk.models.update import (
    TraffixUpdate,
    TraffixUpdateCreate,
    TraffixUpdateRead,
    TraffixUpdateUpdate,
)
from traffix_sdk.models.user import (
    TraffixAPIUser,
    TraffixAPIUserCreate,
    TraffixAPIUserRead,
    TraffixAPIUserUpdate,
)

TraffixUpdateRead.update_forward_refs()
