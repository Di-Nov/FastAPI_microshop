from typing import Annotated

from fastapi import Path, APIRouter

router = APIRouter(prefix='/items', tags=['Items'])


@router.get('/')
def list_items():
    return [
        'items1', 'items2'
    ]


@router.get('/{item_id}')
def get_item_by_id(item_id: Annotated[int, Path(gt=0)]):
    return {
        'item': {item_id}
    }