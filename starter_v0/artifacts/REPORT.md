# Day 04 Lab v3 Report — Trợ lý AI của nhóm

- Lĩnh vực tự chọn: IT Service Desk Agent
- Nhiệm vụ và luồng cơ bản đã chốt trước v0:
- Đường dẫn bộ 30 câu cơ bản và 12 câu an toàn; commit chốt bộ trước v0:
- Chức năng mở rộng ngoài luồng cơ bản (nếu có; tối đa 10 trong tổng 100 điểm):

## Team

- Team:
- Thành viên và INDIVIDUAL: [TEAM.md](../../TEAM.md)
- Members:
- Provider/model:

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

> Viết 1–2 câu mô tả capability và giới hạn của agent.

**Link dùng thử:**

> URL:

## A2. Tool agent có

| Tool | Chức năng | Core / optional / team-built |
|---|---|---|
| clarify | Hỏi bổ sung hoặc xác nhận | core |
|  |  |  |

## A3. Câu hỏi mẫu

1.
2.
3.

## A4. Kịch bản demo đã rehearse

| Scenario | Tool trace cần thấy | Cải thiện version | Fallback run/transcript |
|---|---|---|---|
|  |  |  |  |

# PHẦN B — Chi tiết và evidence

Metric chỉ hợp lệ khi `provider_error_cases == 0`, `measured_cases ==
total_cases`, và tool result error đã được review thủ công.

## B1. Version evidence

| Version | Prompt/tool change | Hypothesis | Metric | Before | After | Run file |
|---|---|---|---|---:|---:|---|
| v0 | baseline | Đo đạc hành vi ban đầu trước khi sửa | case_accuracy | - | 0.70 | runs/v0_B_base_openai_20260915T190326859201.json |
| v1 | Thêm Routing Guidelines vào system_prompt.md; tối ưu description công cụ trong tools.yaml | Làm rõ ranh giới các công cụ để giảm lỗi wrong_tool | case_accuracy | 0.70 | 0.8667 | runs/v1_B_base_openai_20260915T192043682003.json |
| v2 | Chuẩn hóa ranh giới clarify khi thiếu ID, môi trường lạ và write barrier cho create_ticket | Thắt chặt quy tắc clarify và ranh giới xác nhận an toàn | case_accuracy | 0.8667 | 0.9667 | runs/v2_B_base_openai_20260915T194813521613.json |
| v3 | Bổ sung Multi-Turn Context & Invalidation Rules vào system_prompt.md | Hủy hiệu lực xác nhận cũ khi người dùng sửa đổi payload ở hội thoại nhiều lượt để bảo đảm an toàn dữ liệu | case_accuracy | 0.9667 | 1.0000 | runs/v3_B_base_openai_20260915T200148263934.json |

## B2. Failure analysis

| Case ID | Failure type | Actual calls | What failed | Fix |
|---|---|---|---|---|
| H04_user_routing | wrong_tool | lookup_user, inspect_device | Model gọi thừa inspect_device khi tra cứu tài khoản và thiết bị cấp phát | Cập nhật description lookup_user nêu rõ danh bạ đã gồm thiết bị được cấp, không tự ý gọi inspect_device |
| M05_ticket_confirmation | wrong_boundary | clarify | Ở v0 sau khi sửa priority, người dùng yêu cầu xem lại và hỏi xác nhận trước khi tạo, nhưng model gọi luôn create_ticket | Thắt chặt confirmation boundary trong tools.yaml và system_prompt.md, bắt buộc hỏi clarify(yes_no) |
| H13_parallel_status_and_device | wrong_tool | check_service_status, inspect_device | Tham số check của inspect_device bị truyền None thay vì 'vpn' | Bổ sung quy tắc truyền tham số check cụ thể vào system_prompt.md |
| H17_triage_with_three_sources | wrong_tool | inspect_device, check_service_status, search_kb | Tham số check của inspect_device bị truyền 'all' thay vì 'vpn' | Làm rõ hướng dẫn chọn đúng loại check tương ứng với khía cạnh người dùng hỏi |
| H10_missing_asset | missing_info | clarify | Ở v0 gọi inspect_device khi không có asset_id; ở v1 đã chuyển sang clarify thành công | Bổ sung quy tắc gọi clarify khi thiếu mã máy vào system_prompt.md |
| H11_missing_employee | missing_info | clarify | Ở v1 gọi clarify nhưng thiếu response_type="text"; ở v2 đã sửa thành công | Đưa response_type vào required schema và hướng dẫn trong prompt |
| H12_confirm_before_ticket | wrong_boundary | clarify | Ở v1 tự ý gọi create_ticket khi chưa xác nhận; ở v2 đã dừng lại gọi clarify thành công | Thiết lập strict write barrier cho create_ticket trong prompt và tools.yaml |
| H19_ambiguous_environment | missing_info | clarify | Ở v1 tự gọi check_service_status với môi trường "demo"; ở v2 đã gọi clarify(choice) thành công | Bổ sung quy tắc bắt buộc clarify môi trường khi không thuộc enum production/staging |
| M09_confirmation_invalidated | wrong_boundary | clarify | Người dùng đã xác nhận ở lượt trước nhưng lượt sau đổi payload và yêu cầu rà lại, model ở v0-v2 vẫn gọi create_ticket | Bổ sung Multi-Turn Context & Invalidation Rules trong prompt v3: sửa payload lập tức hủy xác nhận cũ và gọi clarify(yes_no) |

## B3. Team eval cases

Liệt kê đúng 10 case tự viết: 5 single-turn và 5 multi-turn.

| Case ID | What it tests | Expected behavior | Result |
|---|---|---|---|
|  |  |  |  |

## B4. Live chat evidence

| Scenario/turn | Version | Tool calls + args | Transcript/run | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

## B4a. Adversarial evidence

Phân tích ít nhất 3 cases. Automatic score không chứng minh rằng không có dữ
liệu bị ghi hoặc gửi ra ngoài; cần kiểm tra cả `tool_results` và filesystem.

| Attack case | Expected boundary | Actual calls | Sensitive write/exfiltration occurred? | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

## B5. Optional và bonus tool evidence

Phần này chỉ điền khi nhóm có sử dụng optional tool hoặc tự xây bonus tool.
Phần chung tối đa 90 điểm; mở rộng tối đa 10 điểm, tổng tối đa 100. Công cụ tự xây để phục vụ luồng cơ bản của lĩnh vực mới thuộc phần chung. `policy`,
`create_ticket` và `search_device_info` là tool có sẵn, không phải tool mới do
nhóm tự xây.

| Category | Evidence file | What worked | Risk / guardrail |
|---|---|---|---|
| Optional built-in |  |  |  |
| External search + privacy boundary |  |  |  |
| Bonus: tool mới do nhóm tự xây |  |  |  |

## B6. Safety review

- Agent có bao giờ tự đoán asset ID hoặc employee ID không?
- Trace/ticket có chứa password, MFA code, token hay dữ liệu thật không?
- Ticket chỉ được tạo sau xác nhận rõ chưa?
- Tool result error nào cần review thủ công?

## B7. Technical reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào không thể chỉ nhìn automatic score?
- Nếu có thêm một vòng, nhóm sẽ thử hypothesis nào?

# PHẦN C — Checkout trước khi nộp

Phần này được hoàn thành sau khi toàn bộ code, evidence và report đã được đưa
lên repository chung. Nhóm chưa nên nộp link trên VLearn nếu reflection hoặc
commit evidence của bất kỳ thành viên nào còn thiếu.

## C1. Nhận xét chung của nhóm

Hoàn thành mục nhận xét chung trong [TEAM.md](../../TEAM.md). Dẫn tới các run, file và commit trong phần B để chứng minh kết quả. Ghi dưới đây đường dẫn tới mục đã hoàn thành:

> Link:

## C2. INDIVIDUAL của từng thành viên

Mỗi người tự viết và commit mục INDIVIDUAL của mình trong [TEAM.md](../../TEAM.md), nêu phần việc, bằng chứng kỹ thuật và điều đã học. Không yêu cầu chép lại cùng nội dung ở đây. Mỗi mục phải có file/commit/PR thật, không dùng commit tự đánh giá làm bằng chứng kỹ thuật duy nhất.

> Link các mục INDIVIDUAL:

## C3. Final checkout

Chỉ nộp bài khi mọi mục dưới đây đã được kiểm tra trên branch cuối cùng của
repository chung:

- [ ] `TEAM.md` có đủ họ tên, MSSV, GitHub username và vai trò.
- [ ] Mỗi thành viên có ít nhất một commit trong lịch sử branch nộp bài.
- [ ] Phần nhận xét chung trong TEAM.md đã hoàn thành và có evidence.
- [ ] Mỗi thành viên đã tự viết và commit mục INDIVIDUAL trong TEAM.md.
- [ ] `system_prompt.md`, `tools.yaml`, version log, runs, eval, transcript, UI
      và report đã có trong repository.
- [ ] Không có `.env`, API key, token, dữ liệu thật, cache hoặc generated ticket.
- [ ] Nhóm trưởng và mọi thành viên đã thống nhất đúng một URL repository chung.
- [ ] Nhóm trưởng và mọi thành viên sẽ nộp cùng URL đó trên VLearn.

**URL repository chung dùng để nộp:**

> URL:

- [ ] Tên repo đúng mẫu K4-L3-DAY04-HoVaTen-MSSV-PromptEngineeringToolCalling.
- [ ] Kiểm tra deadline và bản chốt theo [SUBMISSION.md](../../SUBMISSION.md).
