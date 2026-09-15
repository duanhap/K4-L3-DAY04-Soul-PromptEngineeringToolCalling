# TEAM — Day04, K4-L3B

**Làm nhóm.** Mỗi người tự viết và commit phần INDIVIDUAL của mình.

## Thông tin bài nộp

- Tên nhóm: Soul
- Người đại diện / MSSV: Nguyễn Công Duẩn / 2A202602716
- Tên repo: `K4-L3-DAY04-Soul-PromptEngineeringToolCalling`
- URL repo, nhánh nộp, commit chốt: https://github.com/duanhap/K4-L3-DAY04-Soul-PromptEngineeringToolCalling.git , main , ????
- Deadline áp dụng và link thông báo đổi hạn nếu có: 23:59 16/9/2026

## Thành viên

| Họ và tên | MSSV | GitHub | Vai trò và công việc | File/commit/PR |
|---|---|---|---|---|
| Nguyễn Công Duẩn | [2A202602716] | duanhap | Trưởng nhóm; tạo repo, phân công công việc, chốt workflow, kiểm tra v0-v3, tổng hợp report và final signoff | repo chung, TEAM.md, starter_v0/artifacts/REPORT.md - |
| Phùng Quốc Việt | [2A202602456] | PhungQuocViet |Kỹ sư Prompt Core: Khởi tạo repo/môi trường; tối ưu lặp `system_prompt.md` qua các phiên bản v0->v1->v2->v3 đạt 100% (30/30); thiết kế 10 test case nhóm `data/eval_group.json`; quản lý nhật ký `version_log.csv` và điều phối tích hợp git | `artifacts/system_prompt.md`<br>`data/eval_group.json`<br>`artifacts/version_log.csv`<br>`runs/v0_...` đến `v3_...`<br>Commits: v1, v2-v3, 10 testcase gr |
| Phan Hoàng Vũ | [2A202602450]  | hoangvu180225-cell | Phần UI/chat/transcript: chạy và kiểm tra giao diện, lưu hội thoại, đối chiếu behavior thật với run | starter_v0/README.md,static/app.css + app.js + index.html, ui.py - commit d7e8212 |

## Nhận xét chung

- Kết quả và bằng chứng: Nhóm đã hoàn thành phần kỹ thuật chính của lab: v0-v3 có run hợp lệ, bộ 10 case nhóm đã chạy đạt 10/10, và run adversarial đã kiểm tra ranh giới an toàn. Evidence đang nằm trong starter_v0/runs và starter_v0/artifacts/version_log.csv.
- Thay đổi hiệu quả nhất: cải thiện logic clarify, xác nhận hành động ghi dữ liệu, và chặn stale confirmation / thông tin thiếu nhằm tránh gọi sai tool hoặc tạo ticket sai.
- Giới hạn còn lại: Hệ thống đã đạt chất lượng core, nhưng vẫn còn thiếu các phần mở rộng.
- Cách phân công và tích hợp: Nguyễn Công Duẩn làm trưởng nhóm, tạo repo chung, phân công công việc và giữ tiến độ; Phùng Quốc Việt đảm nhận phần prompt/tool/eval ; Phan Hoàng Vũ phụ trách UI/chat/transcript và demo.

## INDIVIDUAL

Sao chép mục này cho từng thành viên.

### Nguyễn Công Duẩn — [2A202602716]

- Phần việc và file/commit/PR: Trưởng nhóm; tạo repo chung, phân công công việc, theo dõi tiến độ, kiểm tra v0-v3, giữ version_log.csv, tổng hợp bằng chứng và hoàn thiện final checklist. Làm phần còn lại của báo cáo và TEAM.md.
- Quyết định, khó khăn và cách xử lý: Chốt workflow và tiến độ nhóm bằng các mốc v0-v3, ưu tiên run hợp lệ theo provider OpenAI để có bằng chứng thật. Khi có lỗi cấu hình provider hoặc kết quả không đáng tin, tôi xử lý bằng cách xác minh provider_error_cases và chỉ giữ run hợp lệ làm evidence.
- Điều đã học: Mỗi lần sửa prompt/tool phải đi kèm by-case phân tích và run lại để chứng minh cải thiện; chỉ số đẹp không có nghĩa nếu không có bằng chứng kỹ thuật rõ ràng.
- AI/công cụ đã dùng và cách kiểm tra: OpenAI GPT-4o-mini, hệ thống prompt/tool trong starter_v0, chạy kiểm tra qua python run_eval.py và đọc file JSON summary, tool_results, và version_log.csv để đối chiếu.
- Thời điểm đã tự nộp URL repo chung trên VLearn: [00:10:13 16/9/2026]

### Phùng Quốc Việt — [2A202602456]

- Phần việc và file/commit/PR:
  - Khởi tạo môi trường ảo, cấu hình adapter provider OpenAI gpt-4o-mini và giải quyết xung đột thư viện.
  - Phụ trách chính kiến trúc prompt: xây dựng `artifacts/system_prompt.md`, phân tích failure trace từ v0 và lặp qua v1, v2, chốt v3 đạt 30/30 (100%).
  - Phối hợp tinh chỉnh schema `artifacts/tools.yaml` (đưa `response_type` vào `required`, phân định enum).
  - Thiết kế giải pháp phân định ranh giới Read Tools (thực thi ngay) vs Write Tools (bắt buộc xác nhận) và xử lý ngữ cảnh đa lượt (nhớ mã máy, cập nhật thông tin, hủy lệnh).
  - Quản lý nhật ký thử nghiệm `artifacts/version_log.csv`, dọn dẹp các run rác và đồng bộ bằng chứng lên branch `vietpq`.
- Quyết định, khó khăn và cách xử lý: Khắc phục lỗi rate limit 429 quota bằng cách chuyển sang OpenAI gpt-4o-mini để đảm bảo run sạch; thiết lập ranh giới Read/Write tool để vừa tránh over-clarify ở H06 vừa đảm bảo xác nhận ở H12; phân tách rõ mã máy và mã nhân viên để triệt tiêu lỗi đoán mò ID.
- Điều đã học: Nắm vững cơ chế Tool Calling của LLM, kỹ thuật Prompt Engineering có cấu trúc, phương pháp tối ưu lặp có đối chứng và kỹ năng điều phối dự án nhóm trên Git.
- AI/công cụ đã dùng và cách kiểm tra: Sử dụng trợ lý AI hỗ trợ gợi ý ý tưởng; luôn tự kiểm chứng bằng cách chạy thực tế `run_eval.py` trên môi trường thật để kiểm tra trace.
- Thời điểm đã tự nộp URL repo chung trên VLearn: [00:27 ngày 16/09/2026]

### Phan Hoàng Vũ — [2A202602450]

- Phần việc và file/commit/PR:
- Quyết định, khó khăn và cách xử lý:
- Điều đã học:
- AI/công cụ đã dùng và cách kiểm tra:
- Thời điểm đã tự nộp URL repo chung trên VLearn: