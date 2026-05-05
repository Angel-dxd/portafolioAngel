# Portafolio · Angel Xavier Pons Márquez

> Desarrollador Junior Fullstack — especializado en backend.
> Valencia, España · 2026

🌐 **Live:** [angel-dxd.github.io/portafolioAngel](https://angel-dxd.github.io/portafolioAngel/)

---

## 📌 Sobre el proyecto

Portafolio personal estático construido con **HTML + CSS + JavaScript vanilla**, sin frameworks pesados. Optimizado para rendimiento, SEO y accesibilidad, con soporte multi-idioma (ES/EN), modo claro/oscuro adaptativo y animaciones nativas.

El sitio reúne mi perfil profesional, stack técnico, proyectos destacados, formación y CV descargable en ambos idiomas.

---

## 🛠 Stack

| Categoría | Tecnologías |
|-----------|-------------|
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Iconify |
| **Diseño** | CSS Grid, Flexbox, Custom Properties, animaciones CSS |
| **Hosting** | GitHub Pages |
| **CV** | Generación automática vía Python (`cv/generate_cv.py`) |
| **i18n** | Sistema propio de traducción ES/EN basado en `data-i18n` |

---

## 📂 Estructura

```
portafolioAngel/
├── index.html          # Página principal (SPA estática)
├── style.css           # Estilos completos
├── favicon.svg         # Icono del sitio
├── cv/
│   ├── cv_es.pdf       # Currículum en español
│   ├── cv_en.pdf       # Currículum en inglés
│   └── generate_cv.py  # Script generador del CV
└── img/                # Avatar y capturas de proyectos
```

---

## ✨ Características

- **Responsive** — diseño fluido desde móvil hasta 4K
- **Bilingüe** — toggle ES/EN con persistencia
- **Cursor personalizado** — efecto interactivo en escritorio
- **Animaciones on-scroll** — IntersectionObserver para fade-in progresivo
- **Typing effect** — rotación de roles en el hero
- **Accesibilidad** — etiquetas ARIA, contraste AAA, navegación por teclado
- **SEO + Open Graph** — metaetiquetas para compartir en redes
- **Cero dependencias de build** — abre `index.html` y funciona

---

## 🚀 Proyectos destacados

| Proyecto | Descripción | Stack |
|----------|-------------|-------|
| **Boutique Market ERP** | Sistema de gestión empresarial completo con dashboard, autenticación y módulos de mercado | Node.js · TypeScript · MySQL · Docker |
| **Onna Digital** | Colaboración profesional en proyectos digitales | Fullstack |
| **StudyAI Pro** | Plataforma educativa con IA integrada | Web · IA |

---

## 💻 Ejecutar localmente

```bash
git clone https://github.com/Angel-dxd/portafolioAngel.git
cd portafolioAngel

# Opción 1: abrir directamente
open index.html

# Opción 2: servidor local
python3 -m http.server 8000
# → http://localhost:8000
```

---

## 📄 Generar CV

```bash
cd cv
python3 generate_cv.py
```

---

## 📬 Contacto

- 🌐 **Web:** [angel-dxd.github.io/portafolioAngel](https://angel-dxd.github.io/portafolioAngel/)
- 💼 **GitHub:** [@Angel-dxd](https://github.com/Angel-dxd)
- 📧 **Email:** angelxavierponsmarquez2018@gmail.com
- 📍 **Ubicación:** Valencia, España

---

## 📝 Licencia

© 2026 Angel Xavier Pons Márquez. Todos los derechos reservados.
El código del portafolio es de uso personal; las imágenes y CV no pueden ser reutilizados sin permiso.
