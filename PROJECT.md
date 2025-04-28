İşte **deployment** ve **future improvements** bölümleri çıkarılmış, sadeleştirilmiş ve revize edilmiş final versiyon:

---

# 🏗️ Software Architecture Specification  
## Project: **Kanban + Post Management Platform**  
**Author:** Hüsam  
**Backend:** Django 5.x  
**Frontend:** Django Template + Tailwind CSS  
**Database:** PostgreSQL

---

## 1. 🎯 **Purpose**

Bu sistem, kullanıcıların görev atayıp yönetebileceği bir **Kanban Board** sunarken, aynı zamanda içerik paylaşımı yapabildiği bir modül içerir. Yetkilendirme, roller, dosya/yorum sistemleri ve modern bir UI (Tailwind CSS) ile tamamlanmış modüler bir yapıya sahiptir.

---

## 2. 🧱 **System Modules**

### 2.1. `users` (Authentication & Authorization)
- Custom User Model
- Login/Register ekranları
- Role-based access (Admin, Member)

### 2.2. `posts` (Post Management)
- CRUD işlemleri (create, read, update, delete)
- Paylaşım detayları ve erişim kontrolü

### 2.3. `tasks` (Kanban Task Management)
- Görev atama, görüntüleme
- Kanban durumlarına göre gruplama
- Yorum ve dosya ekleme

---

## 3. 🎨 **Frontend (Tailwind CSS)**

### Tasarım Prensipleri:
- Mobil uyumlu responsive layout
- 3 kolonlu kanban görünümü (`grid grid-cols-3 gap-4`)
- Task kartları (`rounded-xl bg-white shadow-md p-4`)
- Yorumlar ve attachlar için `modal`, `accordion` bileşenleri
- Formlar `@apply` ile sadeleştirilmiş: `input input-bordered w-full`

### Kullanılan Tailwind Eklentileri:
- `@tailwind/forms`
- `@tailwind/typography`
- `@tailwind/aspect-ratio`

---

## 4. 🗂️ **Model Design (Backend)**

Aşağıdaki modeller sistemin temel veri yapılarıdır:

### 🔐 User
- `username`: string  
- `email`: string  
- `password`: string  
- `is_admin`: boolean  
- `is_active`: boolean  
- `date_joined`: datetime  

### 📝 Post
- `title`: string  
- `content`: text  
- `author`: FK to User  
- `created_at`: datetime  
- `updated_at`: datetime  

### 📌 Task
- `title`: string  
- `description`: text  
- `assigned_to`: FK to User  
- `created_by`: FK to User  
- `status`: enum [TODO, INPROGRESS, DONE]  
- `created_at`: datetime  

### 📎 TaskAttachment
- `task`: FK to Task  
- `file`: file  
- `uploaded_at`: datetime  

### 💬 TaskComment
- `task`: FK to Task  
- `user`: FK to User  
- `text`: text  
- `tagged_users`: M2M to User  
- `created_at`: datetime  

---

## 5. 🔄 **User Flows**

### 5.1. Görev Yönetimi Akışı
1. Admin kullanıcı giriş yapar.
2. Yeni görev atar.
3. Atanan kullanıcı kanban görünümünde görevlerini görür.
4. Görev detayına girip yorum ya da dosya ekleyebilir.
5. Durum değişikliği frontend’de yapılır.

### 5.2. Post Yönetimi Akışı
1. Kullanıcı yeni post oluşturur.
2. Post listelenir, detay sayfası görüntülenir.
3. Güncelleme/silme yalnızca yazar tarafından yapılabilir.

---

## 6. 🔐 **Access Control**

| Role       | Görev Atama | Post Paylaşma | Görev Güncelleme |
|------------|--------------|----------------|------------------|
| Admin      | ✔️           | ✔️             | ✔️ (tüm görevler) |
| Member     | ❌           | ✔️             | ✔️ (kendi görevleri) |

---

## 7. 🧩 **Routing (Django URLConf)**

| Path                        | Method     | Açıklama                    |
|----------------------------|------------|-----------------------------|
| `/login/`                  | GET/POST   | Giriş ekranı                |
| `/register/`               | GET/POST   | Kayıt ekranı                |
| `/posts/`                  | GET        | Post listesi                |
| `/posts/<id>/`             | GET        | Post detay sayfası         |
| `/posts/create/`           | GET/POST   | Yeni post oluşturma        |
| `/tasks/board/`            | GET        | Kanban görünüm             |
| `/tasks/create/`           | GET/POST   | Görev oluşturma            |
| `/tasks/<id>/comment/`     | POST       | Yorum ekleme                |
| `/tasks/<id>/upload/`      | POST       | Dosya ekleme                |

---


Bu haliyle yazılım mimarisini tanımlayan doküman profesyonel bir yazılım mühendisi veya mimar için tamamlanmıştır. İstersen Markdown veya PDF olarak çıktı alacak şekilde de düzenleyebilirim. İlgini çeker mi?