from fastapi import APIRouter

router = APIRouter(prefix="/api")


@router.get("/health")
async def health():
    return {"status": "CodeGuard is running"}


@router.get("/reviews")
async def get_reviews():
    # TODO: fetch from database
    return {"reviews": []}


@router.get("/reviews/{review_id}")
async def get_review(review_id: str):
    # TODO: fetch specific review
    return {"review_id": review_id}


@router.get("/stats")
async def get_stats():
    # TODO: compute from database
    return {"total_reviews": 0, "total_findings": 0, "top_issues": []}
