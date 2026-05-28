
        function toggleMobileMenu() {
            const navLinks = document.getElementById('navLinks');
            navLinks.classList.toggle('active');
        }

        function toggleSidebar() {
            const sidebar = document.querySelector('.modern-sidebar');
            const overlay = document.querySelector('.sidebar-overlay');
            if (sidebar) sidebar.classList.toggle('active');
            if (overlay) overlay.classList.toggle('active');
        }

        function closeSidebar() {
            const sidebar = document.querySelector('.modern-sidebar');
            const overlay = document.querySelector('.sidebar-overlay');
            if (sidebar) sidebar.classList.remove('active');
            if (overlay) overlay.classList.remove('active');
        }

        function toggleNotificationDropdown(event) {
            if (event) event.stopPropagation();
            const dropdown = document.getElementById('notificationDropdown');
            if (!dropdown) return;
            dropdown.classList.toggle('active');
            
            // Close profile dropdown if open
            document.getElementById('profileDropdown')?.classList.remove('active');
        }

        function markAsRead(notifId) {
            fetch(`/notifications/read/${notifId}`, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Refresh UI if needed or just update item style
                        const item = document.querySelector(`[data-notif-id="${notifId}"]`);
                        if (item) {
                            item.classList.remove('notification-item-new');
                            item.classList.add('notification-item-read');
                        }
                    }
                });
        }

        function markAllAsRead() {
            fetch('/notifications/read-all', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const badge = document.getElementById('notifBadge');
                        if (badge) badge.style.display = 'none';
                        const newNotifs = document.querySelectorAll('.notification-item-new');
                        newNotifs.forEach(n => {
                            n.classList.remove('notification-item-new');
                            n.classList.add('notification-item-read');
                        });
                    }
                });
        }

        function toggleProfileDropdown(event) {
            if (event) event.stopPropagation();
            const profileDropdown = document.getElementById('profileDropdown');
            if (!profileDropdown) return;
            profileDropdown.classList.toggle('active');
            
            // Close notification dropdown if open
            document.getElementById('notificationDropdown')?.classList.remove('active');
        }

        // Logout Confirmation Logic
        let logoutUrl = '';
        
        function confirmLogout(event, url) {
            if (event) event.preventDefault();
            logoutUrl = url;
            if (!logoutUrl && event && event.currentTarget) {
                logoutUrl = event.currentTarget.getAttribute('data-logout-url');
            }
            if (!logoutUrl) logoutUrl = '/logout';
            
            const modal = document.getElementById('logoutModal');
            if (modal) {
                modal.style.display = 'flex';
                setTimeout(() => {
                    modal.classList.add('active');
                }, 10);
            }
        }

        function closeLogoutModal() {
            const modal = document.getElementById('logoutModal');
            modal.classList.remove('active');
            setTimeout(() => {
                modal.style.display = 'none';
            }, 300);
        }

        // Global Action Confirmation Modal
        let actionCallback = null;
        function showActionModal(title, text, type, callback) {
            // Create modal if it doesn't exist
            let modal = document.getElementById('globalActionModal');
            if (!modal) {
                const modalHtml = `
                <div id="globalActionModal" class="modal-overlay">
                    <div class="modal" style="max-width: 400px; text-align: center;">
                        <div class="modal-icon" id="actionModalIcon" style="margin: 0 auto 1.5rem;"><i class='bx bx-question-mark'></i></div>
                        <h3 class="modal-title" id="actionModalTitle">Confirm</h3>
                        <p class="modal-text" id="actionModalText">Are you sure you want to proceed?</p>
                        <div class="modal-actions" style="justify-content: center; margin-top: 2rem;">
                            <button onclick="closeActionModal()" class="btn btn-outline" style="min-width: 100px;">Cancel</button>
                            <button id="confirmActionBtn" class="btn" style="min-width: 100px;">Confirm</button>
                        </div>
                    </div>
                </div>`;
                document.body.insertAdjacentHTML('beforeend', modalHtml);
                modal = document.getElementById('globalActionModal');
                
                document.getElementById('confirmActionBtn').addEventListener('click', function() {
                    if (actionCallback) actionCallback();
                    closeActionModal();
                });
            }
            
            document.getElementById('actionModalTitle').innerText = title;
            document.getElementById('actionModalText').innerText = text;
            
            const icon = document.getElementById('actionModalIcon');
            const confirmBtn = document.getElementById('confirmActionBtn');
            
            if (type === 'danger') {
                icon.innerHTML = "<i class='bx bx-error-circle'></i>";
                icon.style.color = "var(--danger-color)";
                icon.style.background = "rgba(239, 68, 68, 0.1)";
                confirmBtn.className = "btn btn-danger";
            } else if (type === 'warning') {
                icon.innerHTML = "<i class='bx bx-error'></i>";
                icon.style.color = "var(--warning-color)";
                icon.style.background = "rgba(245, 158, 11, 0.1)";
                confirmBtn.className = "btn btn-primary";
                confirmBtn.style.background = "var(--warning-color)";
            } else {
                icon.innerHTML = "<i class='bx bx-check-circle'></i>";
                icon.style.color = "var(--secondary-color)";
                icon.style.background = "rgba(16, 185, 129, 0.1)";
                confirmBtn.className = "btn btn-primary";
            }
            
            actionCallback = callback;
            modal.style.display = 'flex';
            setTimeout(() => { modal.classList.add('active'); }, 10);
        }

        function closeActionModal() {
            const modal = document.getElementById('globalActionModal');
            if(modal) {
                modal.classList.remove('active');
                setTimeout(() => {
                    modal.style.display = 'none';
                    actionCallback = null;
                }, 300);
            }
        }

        // Global Utility for copying recipient number
        function copyRecipientNumber(id = 'recipientNumber') {
            const el = document.getElementById(id);
            if (!el) return;
            const number = el.innerText;
            navigator.clipboard.writeText(number).then(() => {
                const btn = event.currentTarget;
                const icon = btn.querySelector('i');
                const originalIcon = icon.className;
                const originalBorder = btn.style.borderColor;
                const originalColor = btn.style.color;
                
                icon.className = 'bx bx-check';
                btn.style.borderColor = '#10b981';
                btn.style.color = '#10b981';
                
                setTimeout(() => {
                    icon.className = originalIcon;
                    btn.style.borderColor = originalBorder;
                    btn.style.color = originalColor;
                }, 2000);
            });
        }

        
        function showMessages() {
            window.location.href = '/messages';
        }

        document.getElementById('confirmLogoutBtn').addEventListener('click', function() {
            if (logoutUrl) {
                performLogoutWithRefresh(logoutUrl);
            }
        });

        // Close modal when clicking outside
        window.addEventListener('click', function(event) {
            const modal = document.getElementById('logoutModal');
            if (event.target === modal) {
                closeLogoutModal();
            }

            // Close dropdowns when clicking outside
            const notificationDropdown = document.getElementById('notificationDropdown');
            const profileDropdown = document.getElementById('profileDropdown');

            if (notificationDropdown && !notificationDropdown.contains(event.target)) {
                notificationDropdown.classList.remove('active');
            }

            if (profileDropdown && !profileDropdown.contains(event.target)) {
                profileDropdown.classList.remove('active');
            }

            // Close sidebar when clicking outside on mobile
            const sidebar = document.querySelector('.modern-sidebar') || document.getElementById('sidebar');
            const toggles = document.querySelectorAll('.mobile-sidebar-toggle, .mobile-menu-btn');

            if (sidebar && window.innerWidth <= 768 && sidebar.classList.contains('active')) {
                let clickedOnToggle = false;
                toggles.forEach(toggle => {
                    if (toggle.contains(event.target)) {
                        clickedOnToggle = true;
                    }
                });

                if (!sidebar.contains(event.target) && !clickedOnToggle) {
                    closeSidebar();
                }
            }

            // Close mobile menu when clicking outside
            const navLinks = document.getElementById('navLinks');
            const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');

            if (navLinks && !navLinks.contains(event.target) && mobileMenuToggle && !mobileMenuToggle.contains(event.target)) {
                navLinks.classList.remove('active');
            }

            // Handle notification item clicks
            const notifItem = event.target.closest('.notification-item');
            if (notifItem && notifItem.dataset.notifId) {
                markAsRead(notifItem.dataset.notifId);
            }

            // Handle logout link clicks
            const logoutLink = event.target.closest('.profile-menu-item.logout');
            if (logoutLink && logoutLink.dataset.logoutUrl) {
                event.preventDefault();
                confirmLogout(event, logoutLink.dataset.logoutUrl);
            }
        });

        // PWA Service Worker Registration and Nuke Old Caches
        let deferredPrompt;
        
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', function() {
                // Force update or unregister old buggy service workers
                navigator.serviceWorker.getRegistrations().then(function(registrations) {
                    for(let registration of registrations) {
                        registration.update();
                    }
                });
                
                // Clear any excessively aggressive caches unconditionally to free locked browsers
                if (window.caches) {
                    caches.keys().then(function(names) {
                        for (let name of names) {
                            if (name === 'umukozi-v1' || name === 'umukozi-v2') {
                                caches.delete(name);
                            }
                        }
                    });
                }

                navigator.serviceWorker.register('/service-worker.js')
                    .then(function(registration) {
                        console.log('ServiceWorker registration successful');
                    })
                    .catch(function(error) {
                        console.log('ServiceWorker registration failed: ', error);
                    });
            });
        }

        // Listen for install prompt
        window.addEventListener('beforeinstallprompt', function(e) {
            e.preventDefault();
            deferredPrompt = e;
            
            // Show install button in navigation
            const installBtn = document.getElementById('pwa-install-btn');
            if (installBtn) {
                installBtn.style.display = 'block';
            }
            
            // Show install banner after 2 minutes (120,000 milliseconds)
            setTimeout(() => {
                showInstallPrompt();
            }, 120000);
        });

        // Show install prompt to user
        function showInstallPrompt() {
            // Create install banner
            const installBanner = document.createElement('div');
            installBanner.id = 'install-banner';
            installBanner.style.cssText = `
                position: fixed;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: linear-gradient(135deg, #10b981, #059669);
                color: white;
                padding: 16px 24px;
                border-radius: 12px;
                box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);
                z-index: 10000;
                display: flex;
                align-items: center;
                gap: 12px;
                font-family: 'Inter', sans-serif;
                animation: slideUp 0.5s ease;
                max-width: 350px;
            `;
            
            installBanner.innerHTML = '';
            installBanner.innerHTML += '<i class="bx bxs-download" style="font-size: 24px;"></i>';
            installBanner.innerHTML += '<div style="flex: 1;">';
            installBanner.innerHTML += '<div style="font-weight: 600; margin-bottom: 4px;">Install Umukozi App</div>';
            installBanner.innerHTML += '<div style="font-size: 14px; opacity: 0.9;">Get the full experience on your device</div>';
            installBanner.innerHTML += '</div>';
            installBanner.innerHTML += '<button onclick=\"installApp()\" style=\"background: white; color: #10b981; border: none; padding: 8px 16px; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 14px;\">Install</button>';
            installBanner.innerHTML += '<button onclick="dismissInstallBanner()" style="background: transparent; color: white; border: 1px solid rgba(255,255,255,0.3); padding: 8px 12px; border-radius: 8px; cursor: pointer; font-size: 18px; line-height: 1;">&times;</button>';
            
            // Add animation
            const style = document.createElement('style');
            let cssText = '@keyframes slideUp {';
            cssText += 'from { transform: translateX(-50%) translateY(100px); opacity: 0; }';
            cssText += 'to { transform: translateX(-50%) translateY(0); opacity: 1; }';
            cssText += '}';
            style.textContent = cssText;
            document.head.appendChild(style);
            
            document.body.appendChild(installBanner);
        }

        // Install the app
        function installApp() {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then(function(choiceResult) {
                    if (choiceResult.outcome === 'accepted') {
                        console.log('User accepted the install prompt');
                    } else {
                        console.log('User dismissed the install prompt');
                    }
                    deferredPrompt = null;
                    dismissInstallBanner();
                });
            }
        }

        // Dismiss install banner
        function dismissInstallBanner() {
            const banner = document.getElementById('install-banner');
            if (banner) {
                banner.style.animation = 'slideUp 0.5s ease reverse';
                setTimeout(() => banner.remove(), 500);
            }
        }

        // Auto-refresh functionality for actions
        function autoRefreshAfterAction(delay = 1000) {
            setTimeout(function() {
                window.location.reload();
            }, delay);
        }

        // Enhanced logout with auto-refresh
        function performLogoutWithRefresh(url) {
            fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message and redirect to home with refresh
                    window.location.href = data.redirect || '/';
                    setTimeout(() => {
                        window.location.reload();
                    }, 500);
                } else {
                    // Fallback to regular redirect
                    window.location.href = url;
                }
            })
            .catch(error => {
                // Fallback to regular redirect on error
                window.location.href = url;
            });
        }

        // Auto-dismiss flash messages after 4 seconds
        document.addEventListener('DOMContentLoaded', function() {
            const flashMessages = document.querySelectorAll('.flash-message');
            flashMessages.forEach(function(message) {
                setTimeout(function() {
                    message.classList.add('removing');
                    setTimeout(function() {
                        message.remove();
                    }, 300);
                }, 4000); // 4 seconds
            });
            
            // Header scroll effect for transparent header
            const header = document.querySelector('.header-transparent');
            if (header) {
                window.addEventListener('scroll', () => {
                    if (window.scrollY > 50) {
                        header.classList.add('scrolled');
                    } else {
                        header.classList.remove('scrolled');
                    }
                });
            }

            // Check for auto-refresh triggers
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('auto_refresh') === 'true') {
                autoRefreshAfterAction(1000);
            }

            // Auto-refresh after form submissions
            const forms = document.querySelectorAll('form[data-auto-refresh="true"]');
            forms.forEach(function(form) {
                form.addEventListener('submit', function() {
                    autoRefreshAfterAction(2000);
                });
            });

            // Auto-refresh after button clicks with data attribute
            const buttons = document.querySelectorAll('button[data-auto-refresh="true"], a[data-auto-refresh="true"]');
            buttons.forEach(function(button) {
                button.addEventListener('click', function(e) {
                    // Don't refresh if it's a logout button (handled separately)
                    if (!this.closest('.logout')) {
                        autoRefreshAfterAction(1500);
                    }
                });
            });

                    });
    