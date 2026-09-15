# CHECKLIST HOÀN THÀNH DỰ ÁN DAY04
> **Đề tài**: K4 Level 3B — Prompt Engineering & Tool Calling  
> **Repo**: `K4-L3-DAY04-HoVaTen-MSSV-PromptEngineeringToolCalling`  
> **Thang điểm**: 100 điểm (90 điểm Phần chung + 10 điểm Bonus kỹ thuật)

---

## 📌 Bảng Tóm Tắt Tiến Độ (Progress Overview)

- [ ] **Phase 0**: Khởi tạo môi trường & Cấu hình ban đầu
- [ ] **Phase 1**: Chạy Baseline v0 & Phân tích lỗi gốc
- [ ] **Phase 2**: Cải tiến vòng lặp v0 → v1 → v2 → v3 (Prompt & Tool Declaration)
- [ ] **Phase 3**: Xây dựng bộ 10 Case kiểm thử của nhóm (`eval_group.json`)
- [ ] **Phase 4**: Kiểm thử an toàn & Bảo mật (`eval_adversarial.json`)
- [ ] **Phase 5**: Xây dựng UI Chat & Thu thập Transcript thực tế
- [ ] **Phase 6**: Chức năng mở rộng Bonus (Tối đa 10 điểm)
- [ ] **Phase 7**: Hoàn thiện Báo cáo (`REPORT.md`) & Hồ sơ nhóm (`TEAM.md`)
- [ ] **Phase 8**: Kiểm tra an toàn trước khi nộp & Submit VLearn

---

## 🛠 Chi Tiết Từng Giai Đoạn (Action Items)

### Phase 0: Khởi tạo môi trường & Cấu hình ban đầu
- [x] **0.1. Cài đặt môi trường ảo (Virtualenv)**:
  ```powershell
  cd starter_v0
  py -3 -m venv .venv
  .\.venv\Scripts\Activate.ps1
  python -m pip install -r requirements.txt
  ```
- [x] **0.2. Thiết lập API Key**:
  - Tạo file `starter_v0/.env` từ `.env.example`.
  - Cấu hình ít nhất 1 Provider hỗ trợ Tool Calling (`OPENROUTER_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, hoặc `ANTHROPIC_API_KEY`).
  - *(Tùy chọn)* Cấu hình `TAVILY_API_KEY` nếu dùng tool `search_device_info`.
- [x] **0.3. Chạy kiểm tra kết nối (Preflight check)**:
  ```powershell
  python scripts/preflight_provider.py --provider <provider_name>
  ```
  *(Đảm bảo trả về PASS trước khi sang bước tiếp theo)*
- [ ] **0.4. Khai báo ban đầu trong `TEAM.md`**:
  - Điền tên nhóm, thông tin thành viên, MSSV, GitHub username.

---

### Phase 1: Chạy Baseline v0 & Phân tích lỗi gốc
> **Mục tiêu**: Lấy bằng chứng v0 nguyên bản (chưa sửa prompt hay tool declaration) làm mốc so sánh.
- [x] **1.1. Chạy eval v0 trên bộ test cơ bản (30 cases)**:
  ```powershell
  python run_eval.py --provider <provider_name> --version v0 --suite base --eval-cases data/eval_base.json
  ```
- [x] **1.2. Kiểm tra điều kiện hợp lệ của run**:
  - [ ] `provider_error_cases == 0` (không có lỗi mạng/quota/provider).
  - [ ] `measured_cases == total_cases` (30/30 cases).
- [x] **1.3. Lưu trữ run & Phân tích lỗi**:
  - Lưu file run JSON trong `starter_v0/runs/`.
  - Liệt kê các case FAIL (do sai tool, sai argument, tự bịa ID, không hỏi lại...).
- [x] **1.4. Ghi nhận vào `starter_v0/artifacts/version_log.csv`**:
  - Ghi dòng baseline `v0` với hash, metrics, path run file.

---

### Phase 2: Cải tiến vòng lặp v0 → v1 → v2 → v3
> **Quy tắc**: Mỗi version gắn liền với 1 Giả thuyết (Hypothesis) rõ ràng; sửa một phần chính của Prompt hoặc Tool Declaration; chạy lại cùng điều kiện bộ test để đo lường.

#### Phiên bản v1: Tối ưu hóa Tool Routing (Chọn đúng công cụ)
- [x] **2.1. Đặt giả thuyết v1**: Ví dụ: *"Làm rõ ranh giới giữa `check_service_status` (dịch vụ chung) và `inspect_device` (thiết bị cụ thể), phân biệt `search_kb` với `policy` trong `tools.yaml` và `system_prompt.md` sẽ giảm lỗi wrong_tool."*
- [x] **2.2. Chỉnh sửa**:
  - Cập nhật `starter_v0/artifacts/system_prompt.md`.
  - Cập nhật mô tả `description` các tools trong `starter_v0/artifacts/tools.yaml`.
- [x] **2.3. Chạy eval v1**:
  ```powershell
  python run_eval.py --provider <provider_name> --version v1 --suite base --eval-cases data/eval_base.json
  ```
- [x] **2.4. Đánh giá & Ghi log**: So sánh Routing Accuracy với v0, ghi vào `version_log.csv`.

#### Phiên bản v2: Tối ưu Argument Extraction & Thiếu thông tin (`clarify`)
- [ ] **2.5. Đặt giả thuyết v2**: Ví dụ: *"Chuẩn hóa schema parameter trong `tools.yaml` (enum environment, enum check, required fields) và hướng dẫn agent gọi `clarify` khi thiếu asset_id hoặc service name sẽ giảm lỗi wrong_arg_value và missing_info."*
- [ ] **2.6. Chỉnh sửa**:
  - Thắt chặt schema tham số trong `tools.yaml`.
  - Thêm quy tắc xử lý thiếu thông tin trong `system_prompt.md`.
- [ ] **2.7. Chạy eval v2**:
  ```powershell
  python run_eval.py --provider <provider_name> --version v2 --suite base --eval-cases data/eval_base.json
  ```
- [ ] **2.8. Đánh giá & Ghi log**: So sánh Argument Accuracy với v1, ghi vào `version_log.csv`.

#### Phiên bản v3: Xử lý Hội thoại nhiều lượt (Multi-turn) & Xác nhận an toàn
- [ ] **2.9. Đặt giả thuyết v3**: Ví dụ: *"Bổ sung quy tắc nhớ ngữ cảnh lượt trước, tôn trọng lệnh hủy/sửa và bắt buộc cờ `confirmed=True` trước khi gọi `create_ticket` sẽ cải thiện multiturn_accuracy và an toàn dữ liệu."*
- [ ] **2.10. Chỉnh sửa**: Hoàn thiện `system_prompt.md` và `tools.yaml` bản hoàn chỉnh.
- [ ] **2.11. Chạy eval v3**:
  ```powershell
  python run_eval.py --provider <provider_name> --version v3 --suite base --eval-cases data/eval_base.json
  ```
- [ ] **2.12. Đánh giá & Ghi log**: Đảm bảo bảng so sánh v0 - v1 - v2 - v3 có số liệu tiến bộ rõ ràng.

---

### Phase 3: Xây dựng bộ 10 Case kiểm thử của nhóm (`eval_group.json`)
> **Yêu cầu Rubric**: Đúng 10 case gốc của nhóm (không copy từ bộ có sẵn), gồm 5 single-turn và 5 multi-turn.
- [ ] **3.1. Viết 5 case single-turn vào `starter_v0/data/eval_group.json`**:
  - Gồm các tình huống: tra cứu người dùng, kiểm tra dịch vụ đặc thù, truy vấn chính sách, yêu cầu thiếu thông tin cần `clarify`.
- [ ] **3.2. Viết 5 case multi-turn vào `starter_v0/data/eval_group.json`**:
  - Lượt 1 hỏi chung → Lượt 2 bổ sung chi tiết.
  - Lượt 1 yêu cầu hành động → Lượt 2 xác nhận (hoặc hủy bỏ).
  - Lượt 1 hỏi A → Lượt 2 đổi ý sang B.
- [ ] **3.3. Kiểm tra tính hợp lệ của format**:
  - Đúng schema: `id`, `phase: "B"`, `suite: "group"`, `failure_type`, `expect: {"tool_calls": [...]}`.
  - Giá trị `failure_type` phải nằm trong: `["wrong_tool", "wrong_arg_value", "wrong_boundary", "unnecessary_tool", "out_of_scope", "missing_info"]`.
- [ ] **3.4. Chạy eval bộ group trên version v3**:
  ```powershell
  python run_eval.py --provider <provider_name> --version v3 --suite group --eval-cases data/eval_group.json
  ```
- [ ] **3.5. Lưu file run kết quả và phân tích vào `REPORT.md` (mục B3)**.

---

### Phase 4: Kiểm thử an toàn & Bảo mật (`eval_adversarial.json`)
> **Yêu cầu Rubric**: Chạy 12 case an toàn, phân tích chuyên sâu ít nhất 3 case.
- [ ] **4.1. Chạy bộ 12 case adversarial với version hoàn thiện (v3)**:
  ```powershell
  python run_eval.py --provider <provider_name> --version v3 --suite adversarial --eval-cases data/eval_adversarial.json
  ```
- [ ] **4.2. Phân tích ít nhất 3 case tiêu biểu** (ghi vào mục B4a của `REPORT.md`):
  - [ ] Case Prompt Injection / Jailbreak (ví dụ ép agent đọc policy bảo mật hoặc bỏ qua quy tắc).
  - [ ] Case Rò rỉ dữ liệu (Exfiltration): Kiểm tra agent có vô tình gửi mã nội bộ, serial, asset ID lên `search_device_info` ra web ngoài không.
  - [ ] Case Ghi dữ liệu trái phép: Kiểm tra agent có tự ý tạo ticket (`create_ticket`) khi chưa có xác nhận từ người dùng không.
- [ ] **4.3. Kiểm tra tính toàn vẹn**:
  - Xác nhận filesystem không bị sinh ticket rác trái quy định.
  - Kiểm tra log tool args không chứa token, password, khóa bảo mật.

---

### Phase 5: Xây dựng UI Chat & Thu thập Transcript thực tế
> **Yêu cầu Rubric**: UI chạy được, minh bạch hiển thị tool call, argument, kết quả/lỗi, version và lưu được transcript hội thoại thật.
- [ ] **5.1. Triển khai giao diện Chat (UI)**:
  - Có thể dùng Web UI (Streamlit / Gradio / HTML-JS) hoặc hoàn thiện giao diện chat terminal tương tác cao trong `starter_v0/chat.py`.
  - Bắt buộc hiển thị rõ trên màn hình:
    - [ ] Phiên bản Artifact đang chạy (ví dụ `v3`).
    - [ ] Tool nào đang được gọi (`tool_name`).
    - [ ] Các tham số truyền vào (`arguments`).
    - [ ] Kết quả trả về từ tool hoặc thông báo lỗi nếu có (`tool_result` / `error`).
- [ ] **5.2. Thu thập 4 kịch bản Transcript bắt buộc (lưu vào `starter_v0/transcripts/`)**:
  - [ ] Kịch bản 1: Yêu cầu bình thường, luồng chuẩn (Happy path).
  - [ ] Kịch bản 2: Người dùng đưa yêu cầu thiếu thông tin → Agent gọi `clarify` để hỏi lại.
  - [ ] Kịch bản 3: Hội thoại nhiều lượt (Multi-turn), người dùng sửa đổi hoặc cập nhật yêu cầu.
  - [ ] Kịch bản 4: Hành động ghi dữ liệu (ví dụ tạo ticket) có bước xác nhận rõ ràng (`confirmed`).

---

### Phase 6: Chức năng mở rộng Bonus (Tối đa 10 điểm)
> **Yêu cầu Rubric**: Một chức năng mới ngoài luồng cơ bản đã chốt, có code tích hợp, dữ liệu, test case và demo.
- [ ] **6.1. Xác định chức năng mới**:
  - *Ví dụ*: Tool tra cứu lịch bảo trì thiết bị (`schedule_maintenance`), kiểm tra SLA của ticket (`check_ticket_sla`), hoặc tính năng kiểm tra điều kiện bảo hành mở rộng.
- [ ] **6.2. Cài đặt kỹ thuật**:
  - [ ] Tạo module tool trong thư mục `starter_v0/tools/<bonus_tool_name>/tool.py`.
  - [ ] Khai báo hàm trong `starter_v0/tools/__init__.py` (`TOOL_FUNCTIONS`).
  - [ ] Khai báo schema trong `starter_v0/artifacts/tools.yaml`.
  - [ ] Cập nhật hướng dẫn gọi tool trong `starter_v0/artifacts/system_prompt.md`.
- [ ] **6.3. Viết test case & chạy kiểm thử**:
  - Bổ sung test case kiểm thử tool này vào bộ test của nhóm.
- [ ] **6.4. Ghi nhận evidence vào mục B5 của `REPORT.md`**.

---

### Phase 7: Hoàn thiện Báo cáo (`REPORT.md`) & Hồ sơ nhóm (`TEAM.md`)
- [ ] **7.1. Hoàn thiện `starter_v0/artifacts/REPORT.md`**:
  - [ ] Phần A: Giới thiệu agent, bảng danh sách công cụ, câu hỏi mẫu, kịch bản demo đã diễn tập.
  - [ ] Phần B:
    - [ ] B1: Bảng so sánh Version Evidence (v0 → v3 với số liệu đầy đủ).
    - [ ] B2: Bảng phân tích Failure Analysis.
    - [ ] B3: Bảng 10 test case nhóm tự viết.
    - [ ] B4: Live Chat Evidence & Transcript links.
    - [ ] B4a: Bảng phân tích chi tiết 3 case Adversarial.
    - [ ] B5: Bằng chứng tính năng Bonus (nếu có).
    - [ ] B6: Đánh giá an toàn (Safety review).
    - [ ] B7: Suy ngẫm kỹ thuật (Technical reflection).
  - [ ] Phần C: Đường dẫn tới `TEAM.md` và kiểm tra checkout cuối cùng.
- [ ] **7.2. Hoàn thiện `TEAM.md`**:
  - [ ] Điền thông tin repo, nhánh, commit chốt.
  - [ ] Hoàn thành mục **Nhận xét chung của nhóm**.
  - [ ] Mỗi thành viên **tự viết và commit** phần **INDIVIDUAL** của mình (nêu rõ file/commit/PR, việc đã làm, kinh nghiệm rút ra, công cụ AI đã dùng và cách kiểm chứng).

---

### Phase 8: Kiểm tra an toàn trước khi nộp & Submit VLearn
- [ ] **8.1. Kiểm tra dọn dẹp bảo mật (Security Checklist)**:
  - [ ] File `.env` **KHÔNG** bị commit vào Git (đã có trong `.gitignore`).
  - [ ] Tuyệt đối không commit API Key, token thật lên GitHub.
  - [ ] Không commit thư mục `.venv/`, `__pycache__/`, file tạm.
  - [ ] Không commit các ticket phát sinh thử nghiệm trong `tickets/`.
- [ ] **8.2. Kiểm tra commit lịch sử Git**:
  - [ ] Tất cả thành viên trong nhóm đều có ít nhất 1 commit kỹ thuật thật sự trên repo.
  - [ ] Lịch sử commit sạch sẽ, thông điệp commit rõ ràng theo từng version (v0, v1, v2, v3).
- [ ] **8.3. Kiểm tra tên Repo & Quyền truy cập**:
  - [ ] Tên repo chuẩn format: `K4-L3-DAY04-HoVaTen-MSSV-PromptEngineeringToolCalling` (Họ tên không dấu của người đại diện).
  - [ ] Repo ở trạng thái Public hoặc cấp quyền truy cập cho Giảng viên/Keycoach.
- [ ] **8.4. Nộp bài trên VLearn**:
  - [ ] **TẤT CẢ các thành viên trong nhóm** đều mở bài tập Day04 trên VLearn và nộp **CÙNG 1 URL** của repo nhóm.
  - [ ] Ghi chú rõ hash commit chốt nộp bài trước deadline (23:59).

---
*Chúc nhóm hoàn thành xuất sắc dự án Day04 với số điểm tối đa 100/100!*
