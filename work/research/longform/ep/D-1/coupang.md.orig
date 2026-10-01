# D-1 쿠팡 줄 (RULES '쿠팡 대상 편 지정' 2026-10-01 20:45)

업로드 때 설명란 맨 위 두 줄로 넣는다(videos.insert). 이미 올린 뒤 videos.update로 고치지 않는다.

```
이 게시물은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.
퇴사 준비 책(이슬기, 위즈덤하우스): https://link.coupang.com/a/hutlDDyiDQ
```

- 둘째 줄 안내 문구는 초안 — firemap-editor 통과(.edit.json) 전에는 "퇴사 준비 책(이슬기, 위즈덤하우스):" 사실 표기만 쓴다(추천·후기·"클릭" 없음).
- `ytupload.upload(..., paid=True)` 필수. 쇼츠·고정 댓글에는 링크 없음.
- 공개 직전 링크 curl 302 다시 확인(상품 내려가면 링크 빼고 paid=False).
