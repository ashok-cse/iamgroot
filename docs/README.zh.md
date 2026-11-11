# IamGroot

[English](../README.md) · **中文** · [हिन्दी](README.hi.md) · [Español](README.es.md) · [Français](README.fr.md) · [العربية](README.ar.md) · [বাংলা](README.bn.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [اردو](README.ur.md) · [Bahasa Indonesia](README.id.md) · [Deutsch](README.de.md) · [日本語](README.ja.md) · [मराठी](README.mr.md) · [Tiếng Việt](README.vi.md)

**你的私人求职助手。**

找工作要花很多时间。IamGroot 帮你完成那些又慢又无聊的部分。它是一个助手，可以在 Claude Code、Codex、ChatGPT、Gemini、Cursor 等 AI 聊天工具里使用。它适用于任何工作、任何国家。

## 它能做什么

1. **了解你。** 它会读你的简历，再问你几个问题，比如你想在哪里工作、什么时候可以开始。
2. **做一份干净的简历。** 它会做一份一页的简历，招聘软件可以准确读取。
3. **找工作。** 它会查看很多公司的招聘页面，留下适合你的职位。
4. **替你申请。** 它会用你的信息填写申请表并提交。如果你的 AI 工具不能使用浏览器，它会把答案写好，由你来提交。
5. **列一张清单。** 每个职位都会记在同一张清单里，这样你随时都能知道申请了哪里、结果如何。
6. **不断学习。** 它会记住你的回答，不会重复问同一个问题。

## 如何开始

你需要一个 AI 聊天工具。要使用全部功能，电脑上还需要安装 Python（一个免费的程序）。

1. 获取 IamGroot。运行下面的命令，或者下载本项目并在你的 AI 工具中打开：

   ```bash
   npx skills add ashok-cse/iamgroot
   ```

2. 对你的 AI 工具说：**"You are IamGroot. Onboard me."**（意思是：你是 IamGroot，请开始了解我。）
3. 把简历交给它，并回答它的问题。
4. 让它帮你找工作并申请。

## 你的信息只属于你

关于你的所有内容都保存在你自己电脑上一个叫 `profile/` 的文件夹里。这些内容绝不会加进本项目，也绝不会分享给别人。

## 它绝不会做的事

- 编造技能、工作经历或答案。只有你知道答案时，它会来问你。
- 创建账号、输入密码，或绕过“我不是机器人”的验证。
- 为了凑数而申请不适合你的职位。

## 更多内容

下面的文件是英文的。

- 它是怎样一步步工作的: [`skills/iamgroot/SKILL.md`](../skills/iamgroot/SKILL.md)
- 它遵守的全部规则: [`skills/iamgroot/references/instructions.md`](../skills/iamgroot/references/instructions.md)
- 它支持哪些 AI 工具: [`skills/iamgroot/references/agents.md`](../skills/iamgroot/references/agents.md)
- 它从真实的求职申请中学到了什么: [`skills/iamgroot/references/lessons.md`](../skills/iamgroot/references/lessons.md)
- 它怎样填写招聘网站上的表格: [`skills/iamgroot/references/ats-playbook.md`](../skills/iamgroot/references/ats-playbook.md)
- 命令: `python3 skills/iamgroot/scripts/iamgroot.py --help`
