# django-China-api

## 开发流程

1. 根据 issue，从 main 分支切出功能分支（命名规则为 <issue号-feature_summary>，例如 #128-bind_email）
2. 解决 issue 并提交 PR 至 main 分支，指定其他开发人员进行 code review（即使功能未开发完成也鼓励将开发中的代码提交，只需要将对应的 PR 标记为 draft 状态就行，这样方便其他人员跟踪此 issue 的进度）。
3. PR 被批准（approve）后，由 PR 提交者自行以 squash 方式合并代码至主分支（squash message 最后应加入 resolve issue号 将此 PR 关联至对应的 issue）。

## 运行项目

1. 克隆项目到本地
2. 安装项目依赖 `poetry install`
3. 生成数据库 `poetry run python manage.py migrate`
4. 启动开发服务器 `poetry run python manage.py runserver`