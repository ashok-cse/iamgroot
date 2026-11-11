# IamGroot

[English](../README.md) · [中文](README.zh.md) · [हिन्दी](README.hi.md) · [Español](README.es.md) · [Français](README.fr.md) · [العربية](README.ar.md) · [বাংলা](README.bn.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [اردو](README.ur.md) · [Bahasa Indonesia](README.id.md) · [Deutsch](README.de.md) · [日本語](README.ja.md) · [मराठी](README.mr.md) · **Tiếng Việt**

**Trợ lý tìm việc riêng của bạn.**

Tìm việc tốn rất nhiều thời gian. IamGroot làm giúp bạn những phần chậm và nhàm chán. Đây là một trợ lý chạy bên trong các công cụ trò chuyện AI như Claude Code, Codex, ChatGPT, Gemini và Cursor. Nó dùng được cho mọi loại công việc, ở mọi quốc gia.

## Nó làm gì

1. **Tìm hiểu về bạn.** Nó đọc CV của bạn và hỏi vài câu, ví dụ bạn muốn làm việc ở đâu và khi nào bạn có thể bắt đầu.
2. **Tạo một bản CV gọn gàng.** Nó tạo một bản CV một trang mà phần mềm tuyển dụng có thể đọc không bị lỗi.
3. **Tìm việc.** Nó xem trang tuyển dụng của nhiều công ty và giữ lại những việc phù hợp với bạn.
4. **Ứng tuyển thay bạn.** Nó điền thông tin của bạn vào đơn ứng tuyển rồi gửi đi. Nếu công cụ AI của bạn không dùng được trình duyệt web, nó sẽ viết sẵn câu trả lời và bạn tự gửi.
5. **Giữ một danh sách.** Mỗi công việc đều được ghi vào một danh sách duy nhất, nên bạn luôn biết mình đã ứng tuyển ở đâu và kết quả ra sao.
6. **Học hỏi.** Nó nhớ câu trả lời của bạn, nên không hỏi lại cùng một câu.

## Cách bắt đầu

Bạn cần một công cụ trò chuyện AI. Để dùng mọi tính năng, máy tính của bạn cũng cần có Python, một chương trình miễn phí.

1. Tải IamGroot. Chạy lệnh này, hoặc tải dự án này về và mở trong công cụ AI của bạn:

   ```bash
   npx skills add ashok-cse/iamgroot
   ```

2. Nói với công cụ AI của bạn: **"You are IamGroot. Onboard me."** (nghĩa là: bạn là IamGroot, hãy bắt đầu tìm hiểu về tôi.)
3. Đưa CV cho nó và trả lời các câu hỏi.
4. Yêu cầu nó tìm việc và ứng tuyển.

## Thông tin của bạn luôn ở bên bạn

Mọi thông tin về bạn được lưu trong một thư mục tên là `profile/` trên máy tính của chính bạn. Chúng không bao giờ được thêm vào dự án này và không bao giờ bị chia sẻ.

## Những điều nó sẽ không bao giờ làm

- Bịa ra kỹ năng, công việc hay câu trả lời. Khi chỉ bạn biết câu trả lời, nó sẽ hỏi bạn.
- Tạo tài khoản, nhập mật khẩu, hay vượt qua bước kiểm tra “Tôi không phải là người máy”.
- Ứng tuyển vào việc không phù hợp với bạn chỉ để có con số lớn hơn.

## Thông tin thêm

Các tệp dưới đây viết bằng tiếng Anh.

- Cách nó hoạt động từng bước: [`skills/iamgroot/SKILL.md`](../skills/iamgroot/SKILL.md)
- Toàn bộ quy tắc nó tuân theo: [`skills/iamgroot/references/instructions.md`](../skills/iamgroot/references/instructions.md)
- Nó dùng được với những công cụ AI nào: [`skills/iamgroot/references/agents.md`](../skills/iamgroot/references/agents.md)
- Những gì nó học được từ các đơn ứng tuyển thật: [`skills/iamgroot/references/lessons.md`](../skills/iamgroot/references/lessons.md)
- Cách nó điền đơn trên các trang tuyển dụng: [`skills/iamgroot/references/ats-playbook.md`](../skills/iamgroot/references/ats-playbook.md)
- Các lệnh: `python3 skills/iamgroot/scripts/iamgroot.py --help`
