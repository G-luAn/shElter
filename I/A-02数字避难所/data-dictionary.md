# 数据字典

## 一、核心实体

### 1.1 用户（User）

| 字段名 | 数据类型 | 必填 | 说明 |
|-------|---------|------|------|
| user_id | UUID | 是 | 用户唯一标识符 |
| username | VARCHAR(50) | 是 | 用户名，用于登录 |
| email | VARCHAR(100) | 是 | 邮箱地址，用于验证和通知 |
| password_hash | VARCHAR(255) | 是 | 密码哈希值 |
| avatar_url | VARCHAR(500) | 否 | 头像图片 URL |
| bio | TEXT | 否 | 用户简介 |
| role | ENUM | 是 | 用户角色：founder/admin/member |
| status | ENUM | 是 | 账号状态：active/banned/pending |
| created_at | DATETIME | 是 | 注册时间 |
| updated_at | DATETIME | 是 | 最后更新时间 |

### 1.2 社群（Community）

| 字段名 | 数据类型 | 必填 | 说明 |
|-------|---------|------|------|
| community_id | UUID | 是 | 社群唯一标识符 |
| name | VARCHAR(100) | 是 | 社群名称 |
| slug | VARCHAR(100) | 是 | URL 友好名称，用于访问路径 |
| description | TEXT | 是 | 社群简介 |
| cover_url | VARCHAR(500) | 否 | 封面图片 URL |
| owner_id | UUID | 是 | 创始人用户 ID（外键） |
| entry_fee | DECIMAL(10,2) | 否 | 入门费用，为空表示免费 |
| is_private | BOOLEAN | 是 | 是否私密社群 |
| status | ENUM | 是 | 社群状态：active/closed/suspended |
| member_count | INT | 是 | 当前成员数量 |
| created_at | DATETIME | 是 | 创建时间 |
| updated_at | DATETIME | 是 | 更新时间 |

### 1.3 入门问题（EntryQuestion）

| 字段名 | 数据类型 | 必填 | 说明 |
|-------|---------|------|------|
| question_id | UUID | 是 | 问题唯一标识符 |
| community_id | UUID | 是 | 所属社群 ID（外键） |
| question_text | TEXT | 是 | 问题内容 |
| question_order | INT | 是 | 问题顺序号 |
| is_required | BOOLEAN | 是 | 是否必答 |
| created_at | DATETIME | 是 | 创建时间 |

### 1.4 加入申请（JoinApplication）

| 字段名 | 数据类型 | 必填 | 说明 |
|-------|---------|------|------|
| application_id | UUID | 是 | 申请唯一标识符 |
| community_id | UUID | 是 | 申请的社群 ID（外键） |
| user_id | UUID | 是 | 申请人用户 ID（外键） |
| status | ENUM | 是 | 申请状态：pending/approved/rejected |
| rejection_reason | TEXT | 否 | 拒绝原因（管理员填写） |
| applied_at | DATETIME | 是 | 申请时间 |
| reviewed_at | DATETIME | 否 | 审核时间 |

### 1.5 申请答案（ApplicationAnswer）

| 字段名 | 数据类型 | 必填 | 说明 |
|-------|---------|------|------|
| answer_id | UUID | 是 | 答案唯一标识符 |
| application_id | UUID | 是 | 所属申请 ID（外键） |
| question_id | UUID | 是 | 对应问题 ID（外键） |
| answer_text | TEXT | 是 | 答案内容 |
| created_at | DATETIME | 是 | 回答时间 |

### 1.6 社群成员（CommunityMember）

| 字段名 | 数据类型 | 必填 | 说明 |
|-------|---------|------|------|
| membership_id | UUID | 是 | 成员关系唯一标识符 |
| community_id | UUID | 是 | 社群 ID（外键） |
| user_id | UUID | 是 | 用户 ID（外键） |
| role | ENUM | 是 | 成员角色：founder/admin/moderator/member |
| joined_at | DATETIME | 是 | 加入时间 |
| status | ENUM | 是 | 成员状态：active/muted/banned |
| muted_until | DATETIME | 否 | 禁言截止时间 |

### 1.7 帖子（Post）

| 字段名 | 数据类型 | 必填 | 说明 |
|-------|---------|------|------|
| post_id | UUID | 是 | 帖子唯一标识符 |
| community_id | UUID | 是 | 所属社群 ID（外键） |
| author_id | UUID | 是 | 作者用户 ID（外键） |
| title | VARCHAR(200) | 否 | 帖子标题 |
| content | TEXT | 是 | 帖子正文内容 |
| status | ENUM | 是 | 帖子状态：published/draft/hidden/deleted |
| like_count | INT | 是 | 点赞数 |
| comment_count | INT | 是 | 评论数 |
| created_at | DATETIME | 是 | 发布时间 |
| updated_at | DATETIME | 是 | 更新时间 |

### 1.8 评论（Comment）

| 字段名 | 数据类型 | 必填 | 说明 |
|-------|---------|------|------|
| comment_id | UUID | 是 | 评论唯一标识符 |
| post_id | UUID | 是 | 所属帖子 ID（外键） |
| author_id | UUID | 是 | 评论者用户 ID（外键） |
| parent_id | UUID | 否 | 父评论 ID（用于回复） |
| content | TEXT | 是 | 评论内容 |
| status | ENUM | 是 | 评论状态：active/hidden/deleted |
| like_count | INT | 是 | 点赞数 |
| created_at | DATETIME | 是 | 评论时间 |
| updated_at | DATETIME | 是 | 更新时间 |

### 1.9 话题标签（Tag）

| 字段名 | 数据类型 | 必填 | 说明 |
|-------|---------|------|------|
| tag_id | UUID | 是 | 标签唯一标识符 |
| community_id | UUID | 是 | 所属社群 ID（外键） |
| name | VARCHAR(50) | 是 | 标签名称 |
| post_count | INT | 是 | 使用该标签的帖子数 |
| created_at | DATETIME | 是 | 创建时间 |

### 1.10 帖子标签关联（PostTag）

| 字段名 | 数据类型 | 必填 | 说明 |
|-------|---------|------|------|
| post_id | UUID | 是 | 帖子 ID（外键） |
| tag_id | UUID | 是 | 标签 ID（外键） |

---

## 二、枚举值说明

### 用户角色（UserRole）

| 值 | 说明 |
|---|------|
| founder | 社群创始人 |
| admin | 平台管理员 |
| member | 普通成员 |

### 账号状态（UserStatus）

| 值 | 说明 |
|---|------|
| pending | 待验证 |
| active | 正常 |
| banned | 被封禁 |

### 社群状态（CommunityStatus）

| 值 | 说明 |
|---|------|
| active | 正常运营 |
| closed | 已关闭 |
| suspended | 被暂停 |

### 申请状态（ApplicationStatus）

| 值 | 说明 |
|---|------|
| pending | 待审核 |
| approved | 已通过 |
| rejected | 已拒绝 |

### 成员角色（MemberRole）

| 值 | 说明 |
|---|------|
| founder | 社群创始人 |
| admin | 社群管理员 |
| moderator | 版主/审核员 |
| member | 普通成员 |

### 成员状态（MemberStatus）

| 值 | 说明 |
|---|------|
| active | 正常 |
| muted | 禁言中 |
| banned | 被踢出 |

### 内容状态（ContentStatus）

| 值 | 说明 |
|---|------|
| published/draft/active | 已发布/正常 |
| hidden | 仅管理员可见 |
| deleted | 已删除 |

---

## 三、索引设计

| 表名 | 索引字段 | 类型 | 说明 |
|-----|---------|------|------|
| user | email | UNIQUE | 登录查询 |
| user | username | UNIQUE | 展示用 |
| community | slug | UNIQUE | URL 访问 |
| community | owner_id | INDEX | 查询某用户创建的社群 |
| join_application | community_id + status | COMPOSITE | 管理员查询待审核申请 |
| join_application | user_id | INDEX | 用户查询自己的申请记录 |
| community_member | community_id + user_id | COMPOSITE | UNIQUE，防止重复加入 |
| post | community_id + created_at | COMPOSITE | 社群内按时间排序 |
| comment | post_id + created_at | COMPOSITE | 帖子内评论列表 |

---

## 四、关系图

```
用户 (User) 1 ─── * 社群成员 (CommunityMember) * ─── 1 社群 (Community)
   │                                              │
   │                                              │
   └── * 加入申请 (JoinApplication) * ───────────┘
                    │
                    └── * 申请答案 (ApplicationAnswer)

社群 (Community) 1 ─── * 入门问题 (EntryQuestion)
      │
      └── 1 ─── * 帖子 (Post) 1 ─── * 评论 (Comment)
                    │
                    └── * 帖子标签关联 (PostTag) * ─── 1 话题标签 (Tag)
```

---

#I #数据字典 #数字避难所