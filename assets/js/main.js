/**
 * CATech Main JavaScript
 * Handles accessible mobile navigation, header scroll elevation, and interaction controls.
 */

document.addEventListener("DOMContentLoaded", () => {
  const header = document.getElementById("main-header");
  const menuButton = document.getElementById("mobile-menu-btn");
  const mobileMenu = document.getElementById("mobile-menu");
  const mobileNavLinks = document.querySelectorAll(".mobile-nav-link");

  // Toggle mobile navigation drawer
  function toggleMobileMenu(forceClose = false) {
    if (!menuButton || !mobileMenu) return;

    const isOpen = menuButton.getAttribute("aria-expanded") === "true";
    const nextState = forceClose ? false : !isOpen;

    menuButton.setAttribute("aria-expanded", String(nextState));
    if (nextState) {
      mobileMenu.classList.remove("hidden");
    } else {
      mobileMenu.classList.add("hidden");
    }
  }

  if (menuButton) {
    menuButton.addEventListener("click", () => toggleMobileMenu());
  }

  // Close mobile navigation when clicking any mobile link
  mobileNavLinks.forEach((link) => {
    link.addEventListener("click", () => {
      toggleMobileMenu(true);
    });
  });

  // Close menu on Escape key press
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && menuButton && menuButton.getAttribute("aria-expanded") === "true") {
      toggleMobileMenu(true);
      menuButton.focus();
    }
  });

  // Elevate header background on scroll
  function handleScroll() {
    if (!header) return;
    if (window.scrollY > 20) {
      header.classList.add("scrolled");
    } else {
      header.classList.remove("scrolled");
    }
  }

  window.addEventListener("scroll", handleScroll, { passive: true });
  handleScroll();

  // Product Portfolio Filtering
  const filterTabs = document.querySelectorAll(".product-filter-tab");
  const productCards = document.querySelectorAll(".product-card");

  function filterProducts(activeCategory, activeTab) {
    filterTabs.forEach((tab) => {
      const isSelected = tab === activeTab;
      tab.setAttribute("aria-selected", String(isSelected));
      tab.setAttribute("tabindex", isSelected ? "0" : "-1");
      if (isSelected) {
        tab.classList.add("text-white", "bg-indigo-600", "shadow-sm", "shadow-indigo-600/30");
        tab.classList.remove("text-slate-400", "hover:text-white", "hover:bg-slate-800/60");
      } else {
        tab.classList.remove("text-white", "bg-indigo-600", "shadow-sm", "shadow-indigo-600/30");
        tab.classList.add("text-slate-400", "hover:text-white", "hover:bg-slate-800/60");
      }
    });

    productCards.forEach((card) => {
      const cardCategories = (card.getAttribute("data-category") || "").split(/\s+/);
      const isMatch = activeCategory === "all" || cardCategories.includes(activeCategory);

      if (isMatch) {
        card.classList.remove("hidden");
        requestAnimationFrame(() => {
          card.classList.remove("product-card-hidden");
        });
      } else {
        card.classList.add("product-card-hidden");
        const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
        if (prefersReducedMotion) {
          card.classList.add("hidden");
        } else {
          setTimeout(() => {
            if (card.classList.contains("product-card-hidden")) {
              card.classList.add("hidden");
            }
          }, 250);
        }
      }
    });
  }

  filterTabs.forEach((tab, index) => {
    tab.addEventListener("click", () => {
      const filterCategory = tab.getAttribute("data-filter") || "all";
      filterProducts(filterCategory, tab);
    });

    // ARIA keyboard navigation for tablist
    tab.addEventListener("keydown", (event) => {
      let nextIndex = null;
      if (event.key === "ArrowRight") {
        nextIndex = (index + 1) % filterTabs.length;
      } else if (event.key === "ArrowLeft") {
        nextIndex = (index - 1 + filterTabs.length) % filterTabs.length;
      } else if (event.key === "Home") {
        nextIndex = 0;
      } else if (event.key === "End") {
        nextIndex = filterTabs.length - 1;
      }

      if (nextIndex !== null) {
        event.preventDefault();
        filterTabs[nextIndex].focus();
        filterTabs[nextIndex].click();
      }
    });
  });

  // Service chip toggle
  const serviceChips = document.querySelectorAll(".service-chip");
  const serviceInput = document.getElementById("contact-service");

  serviceChips.forEach((chip) => {
    chip.addEventListener("click", () => {
      // Deselect all
      serviceChips.forEach((c) => {
        c.classList.remove("border-teal-500", "text-white", "bg-teal-600/20");
        c.classList.add("border-zinc-700", "text-slate-300", "bg-zinc-900");
      });
      // Select clicked
      chip.classList.remove("border-zinc-700", "text-slate-300", "bg-zinc-900");
      chip.classList.add("border-teal-500", "text-white", "bg-teal-600/20");
      // Update hidden input
      if (serviceInput) serviceInput.value = chip.getAttribute("data-service") || "";
    });
  });

  // Dynamic Copyright Year
  const copyrightYearEl = document.getElementById("copyright-year");
  if (copyrightYearEl) {
    copyrightYearEl.textContent = String(new Date().getFullYear());
  }

  // Back to Top Smooth Scroll
  const backToTopBtn = document.getElementById("back-to-top");
  if (backToTopBtn) {
    backToTopBtn.addEventListener("click", () => {
      const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      window.scrollTo({
        top: 0,
        behavior: prefersReducedMotion ? "auto" : "smooth",
      });
      const mainContent = document.getElementById("main-content");
      if (mainContent) {
        mainContent.focus({ preventScroll: true });
      }
    });
  }

  // Accessible Contact Form Validation & Submission Handling
  const contactForm = document.getElementById("contact-form");
  const formStatus = document.getElementById("form-status");

  if (contactForm) {
    const nameInput = document.getElementById("contact-name");
    const emailInput = document.getElementById("contact-email");
    const messageInput = document.getElementById("contact-message");

    const nameError = document.getElementById("contact-name-error");
    const emailError = document.getElementById("contact-email-error");
    const messageError = document.getElementById("contact-message-error");

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    function clearErrors() {
      [nameInput, emailInput, messageInput].forEach((input) => {
        if (!input) return;
        input.removeAttribute("aria-invalid");
        input.classList.remove("input-error");
      });
      [nameError, emailError, messageError].forEach((errEl) => {
        if (!errEl) return;
        errEl.textContent = "";
        errEl.classList.add("hidden");
      });
      if (formStatus) {
        formStatus.textContent = "";
        formStatus.className = "hidden mb-6 p-4 rounded-xl text-sm font-medium";
      }
    }

    function setFieldError(input, errorEl, message) {
      if (input) {
        input.setAttribute("aria-invalid", "true");
        input.classList.add("input-error");
      }
      if (errorEl) {
        errorEl.textContent = message;
        errorEl.classList.remove("hidden");
      }
    }

    [nameInput, emailInput, messageInput].forEach((input) => {
      if (!input) return;
      input.addEventListener("input", () => {
        if (input.getAttribute("aria-invalid") === "true") {
          input.removeAttribute("aria-invalid");
          input.classList.remove("input-error");
          const errorEl = document.getElementById(`${input.id}-error`);
          if (errorEl) {
            errorEl.textContent = "";
            errorEl.classList.add("hidden");
          }
        }
      });
    });

    contactForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      clearErrors();

      let isValid = true;
      let firstInvalidInput = null;

      const nameVal = nameInput ? nameInput.value.trim() : "";
      const emailVal = emailInput ? emailInput.value.trim() : "";
      const messageVal = messageInput ? messageInput.value.trim() : "";

      if (!nameVal) {
        setFieldError(nameInput, nameError, "What should we call you?");
        isValid = false;
        if (!firstInvalidInput) firstInvalidInput = nameInput;
      }

      if (!emailVal) {
        setFieldError(emailInput, emailError, "We need your email to get back to you.");
        isValid = false;
        if (!firstInvalidInput) firstInvalidInput = emailInput;
      } else if (!emailPattern.test(emailVal)) {
        setFieldError(emailInput, emailError, "That doesn't look like a valid email address.");
        isValid = false;
        if (!firstInvalidInput) firstInvalidInput = emailInput;
      }

      if (!messageVal) {
        setFieldError(messageInput, messageError, "Tell us a bit about your project or what you need help with.");
        isValid = false;
        if (!firstInvalidInput) firstInvalidInput = messageInput;
      } else if (messageVal.length < 10) {
        setFieldError(messageInput, messageError, "A little more detail helps us respond meaningfully.");
        isValid = false;
        if (!firstInvalidInput) firstInvalidInput = messageInput;
      }

      if (!isValid) {
        if (firstInvalidInput) firstInvalidInput.focus();
        return;
      }

      // Disable submit button while sending
      const submitBtn = contactForm.querySelector("button[type=submit]");
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = "Sending…";
      }

      try {
        const formData = new FormData(contactForm);
        const response = await fetch("https://api.web3forms.com/submit", {
          method: "POST",
          body: formData,
        });
        const data = await response.json();

        if (data.success) {
          contactForm.reset();
          if (formStatus) {
            formStatus.innerHTML = "Message sent — we'll get back to you within 24 hours. You can also reach us directly at <a href='mailto:consultanythingtech@gmail.com' class='underline hover:text-white font-mono'>consultanythingtech@gmail.com</a>.";
            formStatus.className = "mb-6 p-4 rounded-xl text-sm font-medium bg-emerald-950/80 border border-emerald-800 text-emerald-300 block";
            formStatus.focus();
          }
        } else {
          throw new Error(data.message || "Submission failed");
        }
      } catch (err) {
        if (formStatus) {
          formStatus.innerHTML = "Something went wrong. Please email us directly at <a href='mailto:consultanythingtech@gmail.com' class='underline hover:text-white font-mono'>consultanythingtech@gmail.com</a>.";
          formStatus.className = "mb-6 p-4 rounded-xl text-sm font-medium bg-rose-950/80 border border-rose-800 text-rose-300 block";
          formStatus.focus();
        }
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = `<span>Send Inquiry</span><svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" /></svg>`;
        }
      }
    });
  }

  // Interactive Logo Concepts Modal & SVG Copy Functionality
  const logoModal = document.getElementById("logo-modal");
  const openModalBtns = document.querySelectorAll(".open-logo-modal-trigger");
  const closeModalBtn = document.getElementById("close-logo-modal-btn");

  if (logoModal) {
    openModalBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        if (typeof logoModal.showModal === "function") {
          logoModal.showModal();
        } else {
          logoModal.classList.remove("hidden");
        }
        document.body.style.overflow = "hidden";
      });
    });

    function closeModal() {
      if (typeof logoModal.close === "function") {
        logoModal.close();
      } else {
        logoModal.classList.add("hidden");
      }
      document.body.style.overflow = "";
    }

    if (closeModalBtn) {
      closeModalBtn.addEventListener("click", closeModal);
    }

    logoModal.addEventListener("click", (event) => {
      const rect = logoModal.getBoundingClientRect();
      const isInDialog = (
        rect.top <= event.clientY &&
        event.clientY <= rect.top + rect.height &&
        rect.left <= event.clientX &&
        event.clientX <= rect.left + rect.width
      );
      if (!isInDialog) {
        closeModal();
      }
    });

    logoModal.addEventListener("cancel", () => {
      document.body.style.overflow = "";
    });

    // Copy SVG snippet or direct path to clipboard
    const copySvgBtns = document.querySelectorAll(".copy-svg-btn");
    copySvgBtns.forEach((btn) => {
      btn.addEventListener("click", async () => {
        const svgPath = btn.getAttribute("data-svg-path");
        if (!svgPath) return;

        try {
          const resp = await fetch(svgPath);
          const svgCode = await resp.text();
          await navigator.clipboard.writeText(svgCode);

          const originalText = btn.innerHTML;
          btn.innerHTML = `
            <svg class="w-3.5 h-3.5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
            </svg>
            <span>Copied SVG!</span>
          `;
          btn.classList.add("border-emerald-500", "text-emerald-300");

          setTimeout(() => {
            btn.innerHTML = originalText;
            btn.classList.remove("border-emerald-500", "text-emerald-300");
          }, 2000);
        } catch (e) {
          // Fallback to copying file URL
          try {
            await navigator.clipboard.writeText(window.location.origin + "/" + svgPath);
            btn.textContent = "Path Copied!";
            setTimeout(() => {
              btn.textContent = "Copy SVG";
            }, 2000);
          } catch (_) {}
        }
      });
    });
  }

  // Ambient Hero 2D Canvas Constellation & Data Stream Background
  function initHeroCanvas() {
    const canvas = document.getElementById("hero-canvas");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const heroSection = document.getElementById("hero") || canvas.parentElement;
    const reducedMotionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");

    let width = 0;
    let height = 0;
    let animationFrameId = null;
    let particles = [];
    const PARTICLE_COUNT = 45;
    const CONNECT_DISTANCE = 130;
    const MOUSE_RADIUS = 160;

    const mouse = {
      x: null,
      y: null,
      isActive: false,
    };

    const colors = [
      "rgba(20, 184, 166, ", // #14b8a6 teal-500
      "rgba(45, 212, 191, ", // #2dd4bf teal-400
      "rgba(6, 182, 212, ",  // #06b6d4 cyan-500
    ];

    function resize() {
      if (!canvas || !heroSection) return;
      const rect = heroSection.getBoundingClientRect();
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      width = rect.width;
      height = rect.height;

      canvas.width = Math.floor(width * dpr);
      canvas.height = Math.floor(height * dpr);
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.scale(dpr, dpr);
    }

    class Particle {
      constructor() {
        this.reset(true);
      }

      reset(init = false) {
        this.x = init ? Math.random() * width : Math.random() * width;
        this.y = init ? Math.random() * height : (Math.random() < 0.5 ? 0 : height);
        this.baseRadius = 1.2 + Math.random() * 1.6;
        this.radius = this.baseRadius;
        this.vx = (Math.random() - 0.5) * 0.4;
        this.vy = (Math.random() - 0.5) * 0.4;
        this.colorBase = colors[Math.floor(Math.random() * colors.length)];
        this.alpha = 0.25 + Math.random() * 0.45;
        this.pulseSpeed = 0.015 + Math.random() * 0.02;
        this.pulseOffset = Math.random() * Math.PI * 2;
      }

      update(time) {
        // Floating drift
        this.x += this.vx;
        this.y += this.vy;

        // Boundary wrap
        if (this.x < -10) this.x = width + 10;
        else if (this.x > width + 10) this.x = -10;
        if (this.y < -10) this.y = height + 10;
        else if (this.y > height + 10) this.y = -10;

        // Gentle attraction to active pointer
        if (mouse.isActive && mouse.x !== null && mouse.y !== null) {
          const dx = mouse.x - this.x;
          const dy = mouse.y - this.y;
          const dist = Math.hypot(dx, dy);

          if (dist < MOUSE_RADIUS && dist > 1) {
            const force = (1 - dist / MOUSE_RADIUS) * 0.035;
            this.vx += (dx / dist) * force;
            this.vy += (dy / dist) * force;
          }
        }

        // Dampen velocity to prevent runaway speed
        this.vx *= 0.985;
        this.vy *= 0.985;

        // Minimum drift persistence
        const speed = Math.hypot(this.vx, this.vy);
        if (speed < 0.1) {
          this.vx += (Math.random() - 0.5) * 0.04;
          this.vy += (Math.random() - 0.5) * 0.04;
        }

        this.currentAlpha = this.alpha + Math.sin(time * this.pulseSpeed + this.pulseOffset) * 0.15;
      }

      draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = `${this.colorBase}${Math.max(0.1, Math.min(1, this.currentAlpha))})`;
        ctx.fill();
      }
    }

    function initParticles() {
      particles = [];
      const count = width < 640 ? 25 : PARTICLE_COUNT;
      for (let i = 0; i < count; i++) {
        particles.push(new Particle());
      }
    }

    function drawConnections() {
      const len = particles.length;
      for (let i = 0; i < len; i++) {
        for (let j = i + 1; j < len; j++) {
          const p1 = particles[i];
          const p2 = particles[j];
          const dx = p1.x - p2.x;
          const dy = p1.y - p2.y;
          const distSq = dx * dx + dy * dy;
          const maxDistSq = CONNECT_DISTANCE * CONNECT_DISTANCE;

          if (distSq < maxDistSq) {
            const dist = Math.sqrt(distSq);
            const alpha = (1 - dist / CONNECT_DISTANCE) * 0.18;
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = `rgba(45, 212, 191, ${alpha})`;
            ctx.lineWidth = 0.75;
            ctx.stroke();
          }
        }

        // Connect particle to cursor if within reach
        if (mouse.isActive && mouse.x !== null && mouse.y !== null) {
          const p = particles[i];
          const dx = mouse.x - p.x;
          const dy = mouse.y - p.y;
          const distSq = dx * dx + dy * dy;
          const maxMouseDistSq = MOUSE_RADIUS * MOUSE_RADIUS;
          if (distSq < maxMouseDistSq) {
            const dist = Math.sqrt(distSq);
            const alpha = (1 - dist / MOUSE_RADIUS) * 0.25;
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(mouse.x, mouse.y);
            ctx.strokeStyle = `rgba(20, 184, 166, ${alpha})`;
            ctx.lineWidth = 0.9;
            ctx.stroke();
          }
        }
      }
    }

    function render(time = 0) {
      ctx.clearRect(0, 0, width, height);
      particles.forEach((p) => {
        p.update(time);
        p.draw();
      });
      drawConnections();
    }

    function animate(time) {
      render(time * 0.05);
      animationFrameId = requestAnimationFrame(animate);
    }

    function startAnimation() {
      if (reducedMotionQuery.matches) {
        // Accessibility: Render a single elegant static frame without continuous RAF loop
        render(0);
        return;
      }
      if (!animationFrameId) {
        animationFrameId = requestAnimationFrame(animate);
      }
    }

    function stopAnimation() {
      if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
        animationFrameId = null;
      }
    }

    // IntersectionObserver to pause animation loop when hero is off-screen
    if ("IntersectionObserver" in window && heroSection) {
      const heroObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            startAnimation();
          } else {
            stopAnimation();
          }
        });
      }, { threshold: 0.05 });
      heroObserver.observe(heroSection);
    }

    // Pointer interaction tracking
    if (heroSection) {
      heroSection.addEventListener("mousemove", (e) => {
        const rect = canvas.getBoundingClientRect();
        mouse.x = e.clientX - rect.left;
        mouse.y = e.clientY - rect.top;
        mouse.isActive = true;
      });

      heroSection.addEventListener("mouseleave", () => {
        mouse.isActive = false;
        mouse.x = null;
        mouse.y = null;
      });
    }

    resize();
    initParticles();
    startAnimation();

    if (window.ResizeObserver) {
      const resizeObserver = new ResizeObserver(() => {
        resize();
        if (reducedMotionQuery.matches) render(0);
      });
      resizeObserver.observe(heroSection);
    } else {
      window.addEventListener("resize", () => {
        resize();
        if (reducedMotionQuery.matches) render(0);
      }, { passive: true });
    }

    if (reducedMotionQuery.addEventListener) {
      reducedMotionQuery.addEventListener("change", (e) => {
        if (e.matches) {
          stopAnimation();
          render(0);
        } else {
          startAnimation();
        }
      });
    }
  }

  // Initialize Hero Canvas Constellation
  initHeroCanvas();

  /**
   * Interactive Hero System Architecture & Local-First Console
   */
  function initHeroConsole() {
    const consoleTabs = document.querySelectorAll('.console-tab[role="tab"]');
    const consolePanels = document.querySelectorAll('.console-panel[role="tabpanel"]');
    const btnSimulateMutation = document.getElementById("btn-simulate-mutation");
    const btnRunTrace = document.getElementById("btn-run-trace");
    const localSyncLog = document.getElementById("local-sync-log");
    const syncRailIndicator = document.getElementById("sync-rail-indicator");
    const syncRailText = document.getElementById("sync-rail-text");
    const syncRailSpeed = document.getElementById("sync-rail-speed");
    const localWriteLatency = document.getElementById("local-write-latency");
    const edgeSyncState = document.getElementById("edge-sync-state");
    const agentExecStatus = document.getElementById("agent-exec-status");
    const traceSteps = document.querySelectorAll(".trace-step");

    if (!consoleTabs.length) return;

    function switchConsoleTab(activeTab) {
      consoleTabs.forEach((tab) => {
        const isSelected = tab === activeTab;
        tab.setAttribute("aria-selected", String(isSelected));
        tab.setAttribute("tabindex", isSelected ? "0" : "-1");
        if (isSelected) {
          tab.classList.add("border-teal-400", "text-teal-300", "bg-teal-950/30");
          tab.classList.remove("border-transparent", "text-slate-400", "hover:text-slate-200");
        } else {
          tab.classList.remove("border-teal-400", "text-teal-300", "bg-teal-950/30");
          tab.classList.add("border-transparent", "text-slate-400", "hover:text-slate-200");
        }
      });

      const targetPanelId = activeTab.getAttribute("aria-controls");
      consolePanels.forEach((panel) => {
        if (panel.id === targetPanelId) {
          panel.classList.remove("hidden");
        } else {
          panel.classList.add("hidden");
        }
      });
    }

    consoleTabs.forEach((tab, index) => {
      tab.addEventListener("click", () => switchConsoleTab(tab));

      // ARIA Roving Tabindex & Keyboard Navigation
      tab.addEventListener("keydown", (e) => {
        let nextIndex = null;
        if (e.key === "ArrowRight") {
          nextIndex = (index + 1) % consoleTabs.length;
        } else if (e.key === "ArrowLeft") {
          nextIndex = (index - 1 + consoleTabs.length) % consoleTabs.length;
        } else if (e.key === "Home") {
          nextIndex = 0;
        } else if (e.key === "End") {
          nextIndex = consoleTabs.length - 1;
        }

        if (nextIndex !== null) {
          e.preventDefault();
          consoleTabs[nextIndex].focus();
          switchConsoleTab(consoleTabs[nextIndex]);
        }
      });
    });

    // Local-First Mutation Simulation
    let mutationCounter = 0;
    let isSimulatingMutation = false;
    if (btnSimulateMutation) {
      btnSimulateMutation.addEventListener("click", () => {
        if (isSimulatingMutation) return;
        isSimulatingMutation = true;
        btnSimulateMutation.disabled = true;
        btnSimulateMutation.classList.add("opacity-75");

        mutationCounter++;
        const now = new Date();
        const timeStr = now.toTimeString().split(" ")[0] + "." + String(now.getMilliseconds()).padStart(3, "0");
        const docId = "doc_8f" + Math.random().toString(16).substring(2, 6);

        // Immediate 0ms local state write
        if (localWriteLatency) {
          localWriteLatency.textContent = "0.08ms";
          localWriteLatency.classList.add("text-emerald-300");
        }
        if (syncRailIndicator) {
          syncRailIndicator.className = "w-2 h-2 rounded-full bg-amber-400 animate-ping";
        }
        if (syncRailText) {
          syncRailText.textContent = `CRDT Delta Rail: Syncing delta (1 pending)...`;
        }
        if (edgeSyncState) {
          edgeSyncState.textContent = "Merging...";
          edgeSyncState.className = "text-amber-400 font-bold";
        }

        // Add log entry and cap to 15 entries
        if (localSyncLog) {
          const logEntry = document.createElement("div");
          logEntry.className = "text-teal-300 font-mono";
          logEntry.innerHTML = `[${timeStr}] <span class="text-white font-bold">MUTATION #${mutationCounter}:</span> Local write committed (0ms) &rarr; broadcasting delta (${docId})`;
          localSyncLog.appendChild(logEntry);
          while (localSyncLog.children.length > 15) {
            localSyncLog.removeChild(localSyncLog.firstElementChild);
          }
          localSyncLog.scrollTop = localSyncLog.scrollHeight;
        }

        // Asynchronous Edge CRDT Sync Resolution
        setTimeout(() => {
          if (syncRailIndicator) {
            syncRailIndicator.className = "w-2 h-2 rounded-full bg-emerald-400 animate-pulse";
          }
          if (syncRailText) {
            syncRailText.textContent = `CRDT Delta Sync Rail: Idle (0 pending)`;
          }
          if (syncRailSpeed) {
            syncRailSpeed.textContent = `Edge P99: ${(14 + Math.floor(Math.random() * 8))}ms`;
          }
          if (edgeSyncState) {
            edgeSyncState.textContent = "State Merged";
            edgeSyncState.className = "text-emerald-400 font-bold";
          }
          if (localSyncLog) {
            const confirmEntry = document.createElement("div");
            confirmEntry.className = "text-emerald-400 font-mono";
            confirmEntry.innerHTML = `&gt; Cloudflare D1 confirmed state vector match (vector_clock: ${mutationCounter + 124})`;
            localSyncLog.appendChild(confirmEntry);
            while (localSyncLog.children.length > 15) {
              localSyncLog.removeChild(localSyncLog.firstElementChild);
            }
            localSyncLog.scrollTop = localSyncLog.scrollHeight;
          }
          btnSimulateMutation.disabled = false;
          btnSimulateMutation.classList.remove("opacity-75");
          isSimulatingMutation = false;
        }, 400);
      });
    }

    // AI Agent Trace Pipeline Execution
    let isRunningTrace = false;
    if (btnRunTrace) {
      btnRunTrace.addEventListener("click", () => {
        if (isRunningTrace) return;
        isRunningTrace = true;
        btnRunTrace.disabled = true;
        btnRunTrace.classList.add("opacity-75");

        if (agentExecStatus) {
          agentExecStatus.textContent = "Executing...";
          agentExecStatus.className = "text-amber-400 font-bold";
        }

        traceSteps.forEach((step) => {
          step.classList.remove("border-teal-500", "bg-teal-950/40");
          step.classList.add("opacity-40");
        });

        // Step through the pipeline sequentially
        const stepDelays = [150, 350, 600, 850];
        stepDelays.forEach((delay, idx) => {
          setTimeout(() => {
            if (traceSteps[idx]) {
              traceSteps[idx].classList.remove("opacity-40");
              traceSteps[idx].classList.add("border-teal-500", "bg-teal-950/40");
            }

            if (idx === stepDelays.length - 1) {
              if (agentExecStatus) {
                agentExecStatus.textContent = "Completed (124ms total)";
                agentExecStatus.className = "text-emerald-400 font-bold";
              }
              btnRunTrace.disabled = false;
              btnRunTrace.classList.remove("opacity-75");
              isRunningTrace = false;
            }
          }, delay);
        });
      });
    }
  }

  // 3D Card Hover Tilt and Pointer Spotlight Shaders
  function initSpotlightAndTilt() {
    const cards = document.querySelectorAll(".spotlight-card");
    if (!cards.length) return;

    const prefersReducedMotion = () =>
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    cards.forEach((card) => {
      card.addEventListener("pointermove", (e) => {
        if (e.pointerType === "touch" || prefersReducedMotion()) return;

        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        card.style.setProperty("--mouse-x", `${x}px`);
        card.style.setProperty("--mouse-y", `${y}px`);

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = ((y - centerY) / centerY) * -5.0;
        const rotateY = ((x - centerX) / centerX) * 5.0;

        card.style.transform = `perspective(1000px) translateY(-4px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) scale3d(1.01, 1.01, 1.01)`;
      });

      card.addEventListener("pointerleave", () => {
        card.style.transform = "";
      });
    });
  }

  // Scroll-Triggered Reveal Animations
  function initScrollReveals() {
    const reveals = document.querySelectorAll(".reveal-on-scroll");
    if (!reveals.length) return;

    const prefersReducedMotion = () =>
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (prefersReducedMotion() || !("IntersectionObserver" in window)) {
      reveals.forEach((el) => el.classList.add("is-revealed"));
      return;
    }

    const observer = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-revealed");
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: "0px 0px -40px 0px" }
    );

    reveals.forEach((el) => observer.observe(el));
  }

  // Smooth Numeric Count-Up Animation
  function initCounterAnimations() {
    const counters = document.querySelectorAll("[data-counter-target]");
    if (!counters.length) return;

    const prefersReducedMotion = () =>
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function animateCounter(counter) {
      const target = parseInt(counter.getAttribute("data-counter-target"), 10);
      if (isNaN(target)) return;

      if (prefersReducedMotion()) {
        counter.textContent = String(target);
        return;
      }

      const duration = 1000;
      const startTime = performance.now();

      function updateCounter(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const ease = 1 - (1 - progress) * (1 - progress);
        const currentVal = Math.round(ease * target);
        counter.textContent = String(currentVal);

        if (progress < 1) {
          requestAnimationFrame(updateCounter);
        } else {
          counter.textContent = String(target);
        }
      }

      counter.textContent = "0";
      requestAnimationFrame(updateCounter);
    }

    if (prefersReducedMotion() || !("IntersectionObserver" in window)) {
      counters.forEach((counter) => {
        const target = counter.getAttribute("data-counter-target");
        if (target) counter.textContent = target;
      });
      return;
    }

    const counterObserver = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animateCounter(entry.target);
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.2 }
    );

    counters.forEach((counter) => counterObserver.observe(counter));
  }

  // Initialize Hero Console, 3D Spotlight Tilt, Reveals, and Counters
  initHeroConsole();
  initSpotlightAndTilt();
  initScrollReveals();
  initCounterAnimations();
});
