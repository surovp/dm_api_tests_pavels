from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, StrictStr, Field, ConstrainedDate
from dm_api_account.models.user_envelope_model import Roles, Rating


class ParseMode(Enum):
    COMMON = 'Common'
    INFO = 'Info'
    POST = 'Post'
    CHAT = 'Chat'


class InfoBbText(BaseModel):
    value: StrictStr
    parse_mode: List[ParseMode]


class ColorSchema(Enum):
    MODERN = 'Modern'
    PALE = 'Pale'
    CLASSIC = 'Classic'
    CLASSIC_PALE = 'ClassicPale'
    NIGHT = 'Night'


class PagingSettings:
    posts_per_page: int = Field(alias='postsPerPage')
    comments_per_page:int = Field(alias='commentsPerPage')
    topics_per_page:int = Field(alias='topicsPerPage')
    messages_per_page:int = Field(alias='messagesPerPage')
    entities_per_page:int = Field(alias='entitiesPerPage')


class UserSettings(BaseModel):
    color_schema: List[ColorSchema] = Field(alias='colorSchema')
    nanny_greetings_message = StrictStr = Field(alias='nannyGreetingsMessage')
    paging: PagingSettings


class UserInfo(BaseModel):
    login: StrictStr
    roles: List[Roles]
    medium_picture_url: Optional[StrictStr] = Field(alias='mediumPictureUrl')
    small_picture_url: Optional[StrictStr] = Field(alias='smallPictureUrl')
    status: StrictStr
    rating: Rating
    online: ConstrainedDate
    name: StrictStr
    location: StrictStr
    registration: ConstrainedDate
    icq: StrictStr
    skype: StrictStr
    original_picture_url: Optional[StrictStr] = Field(alias="originalPictureUrl")
    info: InfoBbText
    settings: UserSettings


class UserDetailsEnvelopeModel(BaseModel):
    resource: UserInfo
    metadata: Optional[StrictStr]
