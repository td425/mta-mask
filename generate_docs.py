#!/usr/bin/env python3
"""Generate SendQ-MTA documentation PDF."""

from fpdf import FPDF


FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

# Shorthand font family names used throughout
SANS = "DSans"
MONO = "DMono"
SERIF = "DSerif"


class DocPDF(FPDF):
    """Custom PDF with header/footer for SendQ-MTA docs."""

    def __init__(self):
        super().__init__()
        # Register Unicode TTF fonts
        self.add_font(SANS, "", FONT_DIR + "DejaVuSans.ttf")
        self.add_font(SANS, "B", FONT_DIR + "DejaVuSans-Bold.ttf")
        self.add_font(MONO, "", FONT_DIR + "DejaVuSansMono.ttf")
        self.add_font(MONO, "B", FONT_DIR + "DejaVuSansMono-Bold.ttf")
        self.add_font(SERIF, "", FONT_DIR + "DejaVuSerif.ttf")
        self.add_font(SERIF, "B", FONT_DIR + "DejaVuSerif-Bold.ttf")

    def header(self):
        if self.page_no() > 1:
            self.set_font(SANS, "", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 8, "SendQ-MTA v1.0.0 \u2014 Documentation", align="L")
            self.cell(0, 8, "Zabith Siraj", align="R", new_x="LMARGIN", new_y="NEXT")
            self.set_draw_color(200, 200, 200)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font(SANS, "", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def chapter_title(self, num, title):
        self.set_font(SANS, "B", 18)
        self.set_text_color(25, 60, 120)
        self.ln(4)
        self.cell(0, 12, f"{num}. {title}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(25, 60, 120)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def section_title(self, title):
        self.set_font(SANS, "B", 13)
        self.set_text_color(50, 90, 150)
        self.ln(3)
        self.cell(0, 9, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def sub_section(self, title):
        self.set_font(SANS, "B", 11)
        self.set_text_color(70, 70, 70)
        self.ln(2)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font(SANS, "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def code_block(self, code):
        self.set_font(MONO, "", 8.5)
        self.set_fill_color(240, 240, 245)
        self.set_text_color(30, 30, 30)
        x = self.get_x()
        self.set_x(x + 2)
        for line in code.strip().split("\n"):
            safe = line.replace("\u2014", "--").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
            self.cell(186, 5, "  " + safe, fill=True, new_x="LMARGIN", new_y="NEXT")
            self.set_x(x + 2)
        self.ln(3)

    def bullet(self, text, indent=10):
        self.set_font(SANS, "", 10)
        self.set_text_color(40, 40, 40)
        x0 = self.get_x()
        self.set_x(x0 + indent)
        self.write(5.5, "\u2022 " + text)
        self.ln(6)

    def bold_bullet(self, label, text, indent=10):
        self.set_text_color(40, 40, 40)
        x0 = self.get_x()
        self.set_x(x0 + indent)
        self.set_font(SANS, "", 10)
        self.write(5.5, "\u2022 ")
        self.set_font(SANS, "B", 10)
        self.write(5.5, f"{label}: ")
        self.set_font(SANS, "", 10)
        self.write(5.5, text)
        self.ln(6)

    def config_param(self, key, default, desc):
        self.set_text_color(40, 40, 40)
        x = self.get_x()
        self.set_x(x + 14)
        self.set_font(MONO, "B", 9)
        self.write(5.5, key)
        self.set_font(SANS, "", 9)
        self.write(5.5, f"  (default: {default})")
        self.ln(5.5)
        self.set_x(x + 20)
        self.set_font(SANS, "", 9)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 5, desc)
        self.set_text_color(40, 40, 40)
        self.ln(1)

    def warning_box(self, text):
        self.set_fill_color(255, 248, 230)
        self.set_draw_color(220, 180, 50)
        self.set_font(SANS, "B", 10)
        self.set_text_color(150, 100, 0)
        y = self.get_y()
        self.rect(12, y, 186, 14, style="DF")
        self.set_xy(16, y + 2)
        self.multi_cell(178, 5, f"Warning: {text}")
        self.ln(6)

    def info_box(self, text):
        self.set_fill_color(235, 245, 255)
        self.set_draw_color(70, 130, 200)
        self.set_font(SANS, "", 9.5)
        self.set_text_color(30, 60, 120)
        y = self.get_y()
        self.rect(12, y, 186, 14, style="DF")
        self.set_xy(16, y + 2)
        self.multi_cell(178, 5, text)
        self.ln(6)


def build_pdf():
    pdf = DocPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font(SANS, "B", 36)
    pdf.set_text_color(25, 60, 120)
    pdf.cell(0, 18, "SendQ-MTA", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(SANS, "", 16)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, "Enterprise Mail Transfer Agent", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_draw_color(25, 60, 120)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(10)
    pdf.set_font(SANS, "", 13)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 8, "User & Developer Documentation", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Version 1.0.0", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)
    pdf.set_font(SANS, "B", 13)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 8, "Author: Zabith Siraj", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(SANS, "", 11)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 7, "hello@zabith.in", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)
    pdf.set_font(SANS, "", 10)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 7, "License: MIT", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Python 3.11+ | Linux | Systemd", align="C", new_x="LMARGIN", new_y="NEXT")

    # =========================================================================
    # TABLE OF CONTENTS
    # =========================================================================
    pdf.add_page()
    pdf.set_font(SANS, "B", 22)
    pdf.set_text_color(25, 60, 120)
    pdf.cell(0, 14, "Table of Contents", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    toc = [
        ("1", "Overview"),
        ("2", "Installation & Setup"),
        ("3", "Configuration Reference"),
        ("4", "CLI Command Reference"),
        ("5", "Server Operations"),
        ("6", "User Management"),
        ("7", "Queue Management"),
        ("8", "Email Authentication (DKIM, SPF, DMARC)"),
        ("9", "TLS & Security"),
        ("10", "Rate Limiting"),
        ("11", "Relay & Delivery"),
        ("12", "Logging & Monitoring"),
        ("13", "Architecture & Developer Guide"),
        ("14", "Troubleshooting"),
        ("15", "FAQ"),
    ]
    for num, title in toc:
        pdf.set_font(SANS, "", 12)
        pdf.set_text_color(40, 40, 40)
        pad = "  " if len(num) == 1 else ""
        pdf.cell(0, 8, f"  {pad}{num}.   {title}", new_x="LMARGIN", new_y="NEXT")

    # =========================================================================
    # 1. OVERVIEW
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("1", "Overview")
    pdf.body_text(
        "SendQ-MTA is a high-performance, enterprise-grade Mail Transfer Agent (MTA) "
        "built in Python 3.11+. It provides a full-featured SMTP server with relay support, "
        "persistent disk-backed queue, DKIM signing, SPF/DMARC verification, TLS encryption, "
        "rate limiting, and user management."
    )
    pdf.section_title("Key Features")
    features = [
        "High-performance async I/O engine with configurable worker pools",
        "SMTP relay with failover support and connection pooling",
        "Direct MX delivery with DNS-based routing",
        "Persistent disk-backed message queue with automatic retry",
        "DKIM signing (RSA-SHA256, Ed25519-SHA256)",
        "SPF checking with configurable policy enforcement",
        "DMARC enforcement with alignment checking",
        "TLS support: STARTTLS (ports 25, 587) and Implicit TLS (port 465)",
        "Multi-tier rate limiting: per-IP, per-domain, per-user, global",
        "User management with Argon2/bcrypt password hashing",
        "YAML configuration with hot-reload via SIGHUP",
        "Prometheus metrics exporter",
        "Systemd integration with full security hardening",
        "Management API via UNIX socket",
    ]
    for f in features:
        pdf.bullet(f)
    pdf.ln(4)

    pdf.section_title("System Requirements")
    pdf.bold_bullet("Operating System", "Linux (systemd-based)")
    pdf.bold_bullet("Python", "3.11 or later (3.11, 3.12, 3.13 supported)")
    pdf.bold_bullet("Privileges", "Root for installation; runs as 'sendq' user")
    pdf.bold_bullet("Network", "Ports 25, 587, 465 (configurable)")
    pdf.bold_bullet("DNS", "MX record pointing to the server for inbound mail")
    pdf.bold_bullet("Reverse DNS", "PTR record matching the HELO hostname")

    # =========================================================================
    # 2. INSTALLATION & SETUP
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("2", "Installation & Setup")

    pdf.section_title("Quick Install")
    pdf.body_text("Run the installation script as root:")
    pdf.code_block("sudo bash scripts/install.sh")

    pdf.body_text("The installation script performs the following steps:")
    steps = [
        "Checks Python 3.11+ is available on the system",
        "Creates system user 'sendq' and group 'sendq' (no login shell)",
        "Creates all required directories with proper ownership",
        "Auto-generates a self-signed TLS certificate (snakeoil) if none exists",
        "Creates a Python virtual environment at /usr/local/lib/sendq-mta",
        "Installs the package with all dependencies: pip install .[full]",
        "Creates CLI symlinks: /usr/bin/sendq-mta and /usr/local/bin/sendq-mta",
        "Installs config files to /etc/sendq-mta/ (preserves existing)",
        "Installs and enables the systemd service unit",
    ]
    for i, s in enumerate(steps, 1):
        pdf.bullet(f"{i}. {s}")
    pdf.ln(4)

    pdf.section_title("Directory Structure")
    pdf.code_block(
        "/etc/sendq-mta/                  # Configuration\n"
        "  sendq-mta.yml                  # Main configuration file\n"
        "  users.yml                      # Internal user database\n"
        "  aliases.yml                    # Email alias mappings\n"
        "  certs/                         # TLS certificates\n"
        "    snakeoil.pem                 # Auto-generated certificate\n"
        "    snakeoil.key                 # Auto-generated private key\n"
        "  dkim/                          # DKIM keys\n"
        "\n"
        "/var/spool/sendq-mta/            # Queue storage\n"
        "  queue/                         # Active messages (pending delivery)\n"
        "  deferred/                      # Deferred messages (retry scheduled)\n"
        "  failed/                        # Permanently failed messages\n"
        "\n"
        "/var/log/sendq-mta/              # Log files\n"
        "  sendq-mta.log                  # Main log (JSON or text)\n"
        "\n"
        "/var/run/sendq-mta/              # Runtime files\n"
        "  sendq-mta.pid                  # PID file\n"
        "  mgmt.sock                      # Management API socket\n"
        "\n"
        "/var/lib/sendq-mta/              # Data directory"
    )

    pdf.section_title("Post-Install Steps")
    pdf.body_text("1. Edit the configuration file:")
    pdf.code_block("sudo nano /etc/sendq-mta/sendq-mta.yml")
    pdf.body_text("2. Set your server hostname (FQDN) -- this is critical for SMTP HELO:")
    pdf.code_block(
        "server:\n"
        '  hostname: "mail.yourdomain.com"'
    )
    pdf.body_text("3. Add your local domains:")
    pdf.code_block(
        "domains:\n"
        "  local_domains:\n"
        '    - "yourdomain.com"'
    )
    pdf.body_text("4. Create a mail user:")
    pdf.code_block("sudo sendq-mta add-user myuser -e myuser@yourdomain.com")
    pdf.body_text("5. Start the server:")
    pdf.code_block("sudo systemctl start sendq-mta\nsudo systemctl enable sendq-mta")

    pdf.section_title("DNS Records Required")
    pdf.body_text("For proper mail delivery, configure these DNS records:")
    pdf.code_block(
        "# A record for mail server\n"
        "mail.yourdomain.com.    IN  A      YOUR_SERVER_IP\n"
        "\n"
        "# MX record for your domain\n"
        "yourdomain.com.         IN  MX  10 mail.yourdomain.com.\n"
        "\n"
        "# PTR (reverse DNS) -- set via your hosting provider\n"
        "YOUR_SERVER_IP          IN  PTR    mail.yourdomain.com.\n"
        "\n"
        "# SPF record\n"
        'yourdomain.com.         IN  TXT    "v=spf1 a mx ip4:YOUR_IP -all"\n'
        "\n"
        "# DKIM record (after generating DKIM keys)\n"
        "sendq._domainkey.yourdomain.com.  IN  TXT  \"v=DKIM1; k=rsa; p=BASE64KEY\"\n"
        "\n"
        "# DMARC record\n"
        '_dmarc.yourdomain.com.  IN  TXT    "v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com"'
    )

    # =========================================================================
    # 3. CONFIGURATION REFERENCE
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("3", "Configuration Reference")
    pdf.body_text(
        "Configuration is stored in YAML format. The config file is searched in this order:"
    )
    pdf.bullet("Path specified with -c flag")
    pdf.bullet("/etc/sendq-mta/sendq-mta.yml")
    pdf.bullet("/etc/sendq-mta/sendq-mta.yaml")
    pdf.bullet("~/.config/sendq-mta/sendq-mta.yml")
    pdf.bullet("./config/sendq-mta.yml")
    pdf.bullet("Built-in defaults (if no file found)")
    pdf.ln(2)
    pdf.info_box("Tip: Use 'sendq-mta validate-config' to check your configuration for errors.")

    # Server section
    pdf.section_title("server.*")
    pdf.config_param("hostname", '"localhost"', "Fully qualified domain name. Used in SMTP HELO/EHLO greeting. Must be a valid FQDN with matching PTR record.")
    pdf.config_param("banner", '"SendQ-MTA Enterprise ESMTP"', "SMTP banner shown to connecting clients.")
    pdf.config_param("pid_file", '"/var/run/sendq-mta/sendq-mta.pid"', "Path to the PID file for the daemon process.")
    pdf.config_param("data_dir", '"/var/lib/sendq-mta"', "Data directory for persistent storage.")
    pdf.config_param("max_message_size", "52428800", "Maximum message size in bytes (default 50 MB).")
    pdf.config_param("trusted_networks", '["127.0.0.0/8", "::1/128"]', "IP addresses/CIDRs allowed to relay mail without authentication.")

    # Listeners
    pdf.section_title("listeners[]")
    pdf.body_text("A list of SMTP listener configurations. Each listener has:")
    pdf.config_param("name", '(required)', "Unique name for the listener (e.g., smtp, submission, smtps).")
    pdf.config_param("address", '"0.0.0.0"', "Bind address. Use 0.0.0.0 for all IPv4 interfaces.")
    pdf.config_param("port", "(required)", "TCP port number. Standard ports: 25, 587, 465.")
    pdf.config_param("tls_mode", '"starttls"', 'TLS mode: "none", "starttls", or "implicit".')
    pdf.config_param("require_auth", "false", "If true, clients must authenticate before sending mail.")
    pdf.config_param("max_connections", "1000", "Maximum simultaneous connections on this listener.")
    pdf.config_param("timeout", "300", "Connection idle timeout in seconds.")

    pdf.body_text("Default listeners configuration:")
    pdf.code_block(
        "listeners:\n"
        '  - name: "smtp"\n'
        '    address: "0.0.0.0"\n'
        "    port: 25\n"
        '    tls_mode: "starttls"\n'
        "    require_auth: false\n"
        "\n"
        '  - name: "submission"\n'
        '    address: "0.0.0.0"\n'
        "    port: 587\n"
        '    tls_mode: "starttls"\n'
        "    require_auth: true\n"
        "\n"
        '  - name: "smtps"\n'
        '    address: "0.0.0.0"\n'
        "    port: 465\n"
        '    tls_mode: "implicit"\n'
        "    require_auth: true"
    )

    # TLS
    pdf.section_title("tls.*")
    pdf.config_param("cert_file", '"/etc/sendq-mta/certs/snakeoil.pem"', "Path to TLS certificate file (PEM format).")
    pdf.config_param("key_file", '"/etc/sendq-mta/certs/snakeoil.key"', "Path to TLS private key file (PEM format).")
    pdf.config_param("ca_file", '""', "Optional CA bundle for client certificate verification.")
    pdf.config_param("min_version", '"TLSv1.2"', 'Minimum TLS version: "TLSv1.2" or "TLSv1.3".')
    pdf.config_param("ciphers", '"ECDHE+AESGCM:..."', "OpenSSL cipher string for allowed cipher suites.")
    pdf.config_param("prefer_server_ciphers", "true", "Prefer server cipher order over client preference.")

    # Relay
    pdf.section_title("relay.*")
    pdf.config_param("enabled", "false", "Enable SMTP relay (smarthost). If false, uses direct MX delivery.")
    pdf.config_param("host", '""', "Relay hostname.")
    pdf.config_param("port", "587", "Relay port (25, 465, 587, 2525).")
    pdf.config_param("username", '""', "SMTP AUTH username for relay.")
    pdf.config_param("password", '""', "SMTP AUTH password for relay.")
    pdf.config_param("auth_method", '"auto"', 'Authentication method: "auto", "plain", "login", "cram-md5".')
    pdf.config_param("tls_mode", '"starttls"', 'Relay TLS mode: "none", "starttls", "implicit".')
    pdf.config_param("tls_verify", "true", "Verify relay server TLS certificate.")
    pdf.config_param("connection_pool_size", "20", "Number of persistent connections to the relay.")
    pdf.config_param("max_connections", "50", "Maximum simultaneous connections to the relay.")
    pdf.config_param("failover", "[]", "List of failover relay servers (same format as primary).")

    # Queue
    pdf.section_title("queue.*")
    pdf.config_param("directory", '"/var/spool/sendq-mta/queue"', "Active queue directory for pending messages.")
    pdf.config_param("deferred_directory", '"/var/spool/sendq-mta/deferred"', "Deferred queue directory for messages awaiting retry.")
    pdf.config_param("failed_directory", '"/var/spool/sendq-mta/failed"', "Failed queue directory for permanently bounced messages.")
    pdf.config_param("workers", "16", "Number of concurrent delivery worker tasks.")
    pdf.config_param("retry_intervals", "[60, 300, 900, ...]", "Exponential backoff schedule in seconds: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 8h, 12h.")
    pdf.config_param("max_retries", "30", "Maximum delivery attempts before permanent failure.")
    pdf.config_param("max_age", "432000", "Maximum message age in seconds (5 days) before bounce.")
    pdf.config_param("flush_interval", "30", "Interval in seconds between deferred queue scans.")

    # Auth
    pdf.section_title("auth.*")
    pdf.config_param("backend", '"internal"', "Authentication backend. Currently only 'internal' is implemented.")
    pdf.config_param("password_hash", '"argon2"', 'Password hashing algorithm: "argon2", "bcrypt", or "sha512".')
    pdf.config_param("users_file", '"/etc/sendq-mta/users.yml"', "Path to internal user database file (YAML).")
    pdf.config_param("min_password_length", "12", "Minimum password length for new users.")

    # Rate limiting
    pdf.section_title("rate_limiting.*")
    pdf.config_param("enabled", "true", "Enable or disable rate limiting globally.")
    pdf.config_param("inbound.max_connections_per_ip", "50", "Max simultaneous connections from a single IP.")
    pdf.config_param("inbound.max_messages_per_ip_per_minute", "100", "Max messages accepted from one IP per minute.")
    pdf.config_param("inbound.max_recipients_per_message", "500", "Max recipients per single message.")
    pdf.config_param("inbound.max_errors_per_ip", "10", "Errors from an IP before automatic ban.")
    pdf.config_param("inbound.ban_duration", "3600", "IP ban duration in seconds (1 hour).")
    pdf.config_param("outbound.max_messages_per_domain_per_minute", "200", "Max outbound messages per destination domain per minute.")
    pdf.config_param("outbound.max_messages_per_second", "500", "Global outbound messages per second (token bucket).")
    pdf.config_param("per_user.max_messages_per_hour", "500", "Per-authenticated-user message limit per hour.")
    pdf.config_param("per_user.max_recipients_per_hour", "2000", "Per-authenticated-user recipient limit per hour.")

    # DKIM / SPF / DMARC
    pdf.section_title("dkim.*")
    pdf.config_param("enabled", "false", "Enable DKIM signing for outbound messages.")
    pdf.config_param("selector", '"sendq"', "DKIM selector name (used in DNS record).")
    pdf.config_param("key_file", '""', "Path to DKIM private key file.")
    pdf.config_param("algorithm", '"rsa-sha256"', 'Signing algorithm: "rsa-sha256" or "ed25519-sha256".')
    pdf.config_param("key_bits", "2048", "RSA key size for key generation.")

    pdf.section_title("spf.*")
    pdf.config_param("enabled", "true", "Enable SPF checking on inbound mail.")
    pdf.config_param("hard_fail_action", '"reject"', 'Action on SPF hard fail: "reject", "quarantine", or "tag".')
    pdf.config_param("soft_fail_action", '"tag"', 'Action on SPF soft fail.')
    pdf.config_param("neutral_action", '"accept"', 'Action on SPF neutral result.')

    pdf.section_title("dmarc.*")
    pdf.config_param("enabled", "true", "Enable DMARC policy enforcement.")
    pdf.config_param("reject_action", '"reject"', 'Action when DMARC policy is p=reject.')
    pdf.config_param("quarantine_action", '"quarantine"', 'Action when DMARC policy is p=quarantine.')

    # Logging
    pdf.section_title("logging.*")
    pdf.config_param("level", '"info"', 'Log level: "debug", "info", "warning", "error".')
    pdf.config_param("file", '"/var/log/sendq-mta/sendq-mta.log"', "Log file path.")
    pdf.config_param("max_size", '"100M"', 'Max log file size before rotation (supports K, M, G suffixes).')
    pdf.config_param("max_files", "30", "Number of rotated log files to retain.")
    pdf.config_param("format", '"json"', 'Log format: "json" (structured) or "text" (human-readable).')

    # =========================================================================
    # 4. CLI COMMAND REFERENCE
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("4", "CLI Command Reference")
    pdf.body_text("All commands use the 'sendq-mta' binary. Global options:")
    pdf.code_block(
        "sendq-mta [--config PATH] [--version] COMMAND [OPTIONS]"
    )

    # Server commands
    pdf.section_title("Server Control")

    pdf.sub_section("sendq-mta start")
    pdf.body_text("Start the MTA server. Daemonizes by default.")
    pdf.code_block("sendq-mta start              # Start as daemon\nsendq-mta start -f           # Run in foreground")
    pdf.bold_bullet("-f, --foreground", "Run in foreground (no daemonization). Useful for debugging or systemd.")

    pdf.sub_section("sendq-mta stop")
    pdf.body_text("Gracefully stop the running server. Sends SIGTERM and waits up to 30 seconds.")
    pdf.code_block("sendq-mta stop")

    pdf.sub_section("sendq-mta restart")
    pdf.body_text("Stop and restart the server.")
    pdf.code_block("sendq-mta restart\nsendq-mta restart -f         # Restart in foreground")

    pdf.sub_section("sendq-mta status")
    pdf.body_text("Show server status, queue statistics, listener configuration, and relay mode.")
    pdf.code_block(
        "$ sendq-mta status\n"
        "SendQ-MTA v1.0.0\n"
        "Config: /etc/sendq-mta/sendq-mta.yml\n"
        "Status: RUNNING (PID 12345)\n"
        "\n"
        "Queue:\n"
        "  Active:   0\n"
        "  Deferred: 0\n"
        "  Failed:   0\n"
        "\n"
        "Listeners:\n"
        "  smtp         0.0.0.0:25 (tls=starttls, auth=False)\n"
        "  submission   0.0.0.0:587 (tls=starttls, auth=True)\n"
        "  smtps        0.0.0.0:465 (tls=implicit, auth=True)\n"
        "\n"
        "Relay: direct delivery (MX lookup)"
    )

    pdf.sub_section("sendq-mta reload")
    pdf.body_text("Reload configuration without restarting. Sends SIGHUP to the daemon.")
    pdf.code_block("sendq-mta reload")

    # User management
    pdf.section_title("User Management")

    pdf.sub_section("sendq-mta add-user <username>")
    pdf.body_text("Create a new mail user. Password is prompted if not provided.")
    pdf.code_block(
        "sendq-mta add-user john\n"
        "sendq-mta add-user john -p 'MySecurePass123' -e john@example.com\n"
        "sendq-mta add-user john --quota 500 --send-limit 100"
    )
    pdf.bold_bullet("-p, --password", "Set password inline (prompted if omitted)")
    pdf.bold_bullet("-e, --email", "User email address")
    pdf.bold_bullet("-d, --display-name", "Display name")
    pdf.bold_bullet("--quota", "Mailbox quota in MB (0 = unlimited)")
    pdf.bold_bullet("--send-limit", "Send limit per hour (0 = use config default)")

    pdf.sub_section("sendq-mta list-users")
    pdf.body_text("List all configured users.")
    pdf.code_block(
        "sendq-mta list-users\n"
        "sendq-mta list-users --format json"
    )

    pdf.sub_section("sendq-mta show-user <username>")
    pdf.body_text("Show detailed information about a specific user.")
    pdf.code_block("sendq-mta show-user john")

    pdf.sub_section("sendq-mta edit-user <username>")
    pdf.body_text("Modify user properties.")
    pdf.code_block(
        "sendq-mta edit-user john --email john@newdomain.com\n"
        "sendq-mta edit-user john --disable\n"
        "sendq-mta edit-user john --enable --quota 1000"
    )

    pdf.sub_section("sendq-mta delete-user <username>")
    pdf.body_text("Delete a user account. Asks for confirmation unless -y is passed.")
    pdf.code_block("sendq-mta delete-user john -y")

    pdf.sub_section("sendq-mta change-pass <username>")
    pdf.body_text("Change a user's password.")
    pdf.code_block("sendq-mta change-pass john\nsendq-mta change-pass john -p 'NewPassword123!'")

    # Queue management
    pdf.section_title("Queue Management")

    pdf.sub_section("sendq-mta queue-status")
    pdf.body_text("Show queue statistics. Use -v for per-message details.")
    pdf.code_block(
        "$ sendq-mta queue-status -v\n"
        "Queue Status:\n"
        "  Active:   2\n"
        "  Deferred: 1\n"
        "  Failed:   0\n"
        "  Total:    3\n"
        "\n"
        "Messages:\n"
        "  ID                              Sender           Rcpts  Retry  Status\n"
        "  sendq-a1b2c3...  user@ex.com    1      0      queued"
    )

    pdf.sub_section("sendq-mta flush-queue")
    pdf.body_text("Delete all messages from the active and deferred queues. Asks for confirmation.")
    pdf.code_block(
        "$ sendq-mta flush-queue\n"
        "  Active:   2\n"
        "  Deferred: 1\n"
        "Delete all 3 messages from the queue? [y/N]: y\n"
        "Flushed 3 messages from the queue.\n"
        "\n"
        "# Skip confirmation:\n"
        "sendq-mta flush-queue -y"
    )

    pdf.sub_section("sendq-mta delete-msg <msg-id>")
    pdf.body_text("Delete a specific message by ID from any queue.")
    pdf.code_block("sendq-mta delete-msg sendq-a1b2c3d4e5f67890-1234567890 -y")

    pdf.sub_section("sendq-mta purge-failed")
    pdf.body_text("Delete all permanently failed messages.")
    pdf.code_block("sendq-mta purge-failed -y")

    # Domain management
    pdf.section_title("Domain Management")

    pdf.sub_section("sendq-mta list-domains")
    pdf.body_text("Show all configured local, relay, and blocked domains.")

    pdf.sub_section("sendq-mta add-domain <domain>")
    pdf.code_block(
        "sendq-mta add-domain example.com              # Add as local domain\n"
        "sendq-mta add-domain partner.com --type relay  # Add as relay domain"
    )

    pdf.sub_section("sendq-mta remove-domain <domain>")
    pdf.code_block("sendq-mta remove-domain old.com --type local")

    # Config & testing
    pdf.section_title("Configuration & Testing")

    pdf.sub_section("sendq-mta validate-config")
    pdf.body_text("Validate the configuration file for errors (missing TLS files, bad relay config, etc.).")

    pdf.sub_section("sendq-mta show-config")
    pdf.body_text("Display the current configuration. Sensitive fields are redacted.")
    pdf.code_block("sendq-mta show-config\nsendq-mta show-config --section relay")

    pdf.sub_section("sendq-mta test-relay")
    pdf.body_text("Test connectivity to the configured relay server (TLS, AUTH, NOOP).")

    pdf.sub_section("sendq-mta test-send")
    pdf.body_text("Send a test email through the local MTA.")
    pdf.code_block(
        'sendq-mta test-send --to user@example.com\n'
        'sendq-mta test-send --to user@example.com --from test@mydomain.com -p 587'
    )

    pdf.sub_section("sendq-mta generate-dkim")
    pdf.body_text("Generate a DKIM key pair and DNS record for a domain.")
    pdf.code_block(
        "sendq-mta generate-dkim -d example.com\n"
        "sendq-mta generate-dkim -d example.com -s myselector -b 4096"
    )

    # =========================================================================
    # 5. SERVER OPERATIONS
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("5", "Server Operations")

    pdf.section_title("Starting with Systemd (Recommended)")
    pdf.code_block(
        "sudo systemctl start sendq-mta       # Start the service\n"
        "sudo systemctl stop sendq-mta        # Stop the service\n"
        "sudo systemctl restart sendq-mta     # Restart the service\n"
        "sudo systemctl enable sendq-mta      # Enable at boot\n"
        "sudo systemctl status sendq-mta      # Check systemd status"
    )

    pdf.section_title("Starting Manually")
    pdf.code_block(
        "sendq-mta start                      # Start as daemon\n"
        "sendq-mta start -f                   # Foreground (for debugging)\n"
        "sendq-mta stop                       # Stop daemon\n"
        "sendq-mta restart                    # Restart"
    )

    pdf.section_title("Signal Handling")
    pdf.body_text("The server responds to these UNIX signals:")
    pdf.bold_bullet("SIGTERM", "Graceful shutdown. Stops workers, closes listeners, cleans up PID file.")
    pdf.bold_bullet("SIGHUP", "Hot-reload configuration from disk without restarting.")
    pdf.bold_bullet("SIGUSR1", "Reload the active queue directory. Used by 'flush-queue' CLI command.")
    pdf.bold_bullet("SIGINT", "Immediate graceful shutdown (same as SIGTERM).")

    pdf.section_title("Configuration Hot-Reload")
    pdf.body_text("Reload config without downtime:")
    pdf.code_block("sendq-mta reload\n# or\nkill -HUP $(cat /var/run/sendq-mta/sendq-mta.pid)")

    pdf.section_title("Systemd Security Hardening")
    pdf.body_text(
        "The systemd service unit includes extensive security hardening. The server runs "
        "as the unprivileged 'sendq' user with only CAP_NET_BIND_SERVICE capability "
        "(to bind ports 25, 587, 465). Protected features include:"
    )
    pdf.bullet("NoNewPrivileges: cannot gain new privileges via setuid/setgid")
    pdf.bullet("ProtectSystem=strict: read-only filesystem except whitelisted paths")
    pdf.bullet("ProtectHome: no access to /home directories")
    pdf.bullet("PrivateTmp: isolated /tmp namespace")
    pdf.bullet("ProtectKernelTunables, ProtectKernelModules, ProtectControlGroups")
    pdf.bullet("RestrictNamespaces, RestrictRealtime, LockPersonality")
    pdf.ln(2)
    pdf.body_text("Resource limits: 65536 open files, 4096 tasks maximum.")

    # =========================================================================
    # 6. USER MANAGEMENT
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("6", "User Management")
    pdf.body_text(
        "SendQ-MTA uses an internal user database stored in YAML format at "
        "/etc/sendq-mta/users.yml. Passwords are hashed using Argon2 (default), "
        "bcrypt, or SHA-512. The file is permission-restricted to mode 0600."
    )
    pdf.warning_box("Never edit users.yml manually. Always use CLI commands.")

    pdf.section_title("User Properties")
    pdf.bold_bullet("username", "Unique login identifier")
    pdf.bold_bullet("email", "User's email address (default: username@hostname)")
    pdf.bold_bullet("display_name", "Human-readable name")
    pdf.bold_bullet("enabled", "Whether the account is active (true/false)")
    pdf.bold_bullet("quota_mb", "Mailbox storage quota in megabytes (0 = unlimited)")
    pdf.bold_bullet("send_limit_per_hour", "Max messages per hour (0 = use global config)")
    pdf.bold_bullet("created_at", "Account creation timestamp (ISO 8601)")
    pdf.bold_bullet("last_login", "Last authentication timestamp (ISO 8601)")

    pdf.section_title("Password Hashing")
    pdf.body_text(
        "Passwords are hashed before storage. Supported algorithms (in order of preference):"
    )
    pdf.bold_bullet("Argon2", "Memory-hard, GPU-resistant. Recommended and default. Requires argon2-cffi.")
    pdf.bold_bullet("bcrypt", "Battle-tested, widely supported. Fallback. Requires bcrypt package.")
    pdf.bold_bullet("SHA-512", "Hash with random salt. Basic fallback, no extra dependencies.")
    pdf.ln(2)
    pdf.body_text("Configure the algorithm in sendq-mta.yml:")
    pdf.code_block('auth:\n  password_hash: "argon2"    # argon2 | bcrypt | sha512\n  min_password_length: 12')

    # =========================================================================
    # 7. QUEUE MANAGEMENT
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("7", "Queue Management")

    pdf.section_title("Message Lifecycle")
    pdf.body_text("Every email message passes through these states:")
    pdf.code_block(
        "INCOMING EMAIL\n"
        "     |\n"
        "     v\n"
        "[QUEUED]  -->  Written to /var/spool/sendq-mta/queue/\n"
        "     |        (.meta.json + .eml per message)\n"
        "     v\n"
        "[DELIVERING]  -->  Delivery worker attempts send\n"
        "     |        |\n"
        "  SUCCESS   FAILURE\n"
        "     |        |\n"
        "  DELETE   [DEFERRED]  -->  Moved to /var/spool/sendq-mta/deferred/\n"
        "              |            Retry scheduled with backoff\n"
        "              v\n"
        "         After max_retries (30) or max_age (5 days)\n"
        "              |\n"
        "              v\n"
        "          [FAILED]  -->  Moved to /var/spool/sendq-mta/failed/\n"
        "                        Permanent failure, bounce notification"
    )

    pdf.section_title("Retry Schedule (Default)")
    pdf.body_text("When delivery fails, messages are retried with exponential backoff:")
    pdf.code_block(
        "Retry 1:   1 minute\n"
        "Retry 2:   5 minutes\n"
        "Retry 3:  15 minutes\n"
        "Retry 4:  30 minutes\n"
        "Retry 5:   1 hour\n"
        "Retry 6:   2 hours\n"
        "Retry 7:   4 hours\n"
        "Retry 8:   8 hours\n"
        "Retry 9+: 12 hours (repeats until max_retries or max_age)"
    )

    pdf.section_title("Queue Operations")
    pdf.body_text("View queue status:")
    pdf.code_block("sendq-mta queue-status -v")
    pdf.body_text("Flush (delete) all queued messages:")
    pdf.code_block("sendq-mta flush-queue -y")
    pdf.body_text("Delete a specific message:")
    pdf.code_block("sendq-mta delete-msg <message-id> -y")
    pdf.body_text("Purge all failed messages:")
    pdf.code_block("sendq-mta purge-failed -y")

    pdf.section_title("On-Disk Format")
    pdf.body_text("Each message is stored as two files:")
    pdf.bold_bullet("{msg_id}.meta.json", "JSON metadata: sender, recipients, timestamps, retry count, status, errors")
    pdf.bold_bullet("{msg_id}.eml", "Raw email message body (RFC 5322 format)")

    # =========================================================================
    # 8. EMAIL AUTHENTICATION
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("8", "Email Authentication (DKIM, SPF, DMARC)")

    pdf.section_title("DKIM Signing")
    pdf.body_text(
        "DomainKeys Identified Mail (DKIM) adds a cryptographic signature to outbound messages, "
        "allowing receiving servers to verify the message was authorized by the sending domain."
    )
    pdf.sub_section("Setup DKIM")
    pdf.body_text("1. Generate DKIM keys:")
    pdf.code_block("sendq-mta generate-dkim -d yourdomain.com -s sendq -b 2048")
    pdf.body_text("2. Add the DNS TXT record printed by the command.")
    pdf.body_text("3. Enable DKIM in configuration:")
    pdf.code_block(
        "dkim:\n"
        "  enabled: true\n"
        '  selector: "sendq"\n'
        '  key_file: "/etc/sendq-mta/dkim/yourdomain.com.sendq.private.pem"\n'
        "  signing_domains:\n"
        '    - "yourdomain.com"\n'
        '  algorithm: "rsa-sha256"'
    )
    pdf.body_text("4. Reload configuration:")
    pdf.code_block("sendq-mta reload")

    pdf.section_title("SPF Checking")
    pdf.body_text(
        "Sender Policy Framework (SPF) validates that the sending IP is authorized to send "
        "mail for the domain in the envelope sender. SPF is checked on all inbound mail."
    )
    pdf.body_text("Configurable actions per SPF result:")
    pdf.bold_bullet("Hard fail (fail)", "Default: reject. Options: reject, quarantine, tag.")
    pdf.bold_bullet("Soft fail (softfail)", "Default: tag. Options: reject, quarantine, tag.")
    pdf.bold_bullet("Neutral", "Default: accept. Options: accept, reject, quarantine, tag.")

    pdf.section_title("DMARC Enforcement")
    pdf.body_text(
        "Domain-based Message Authentication, Reporting and Conformance (DMARC) builds on "
        "SPF and DKIM to verify the From header domain. DMARC checks alignment between the "
        "From domain and SPF/DKIM results."
    )
    pdf.body_text("Alignment modes:")
    pdf.bold_bullet("Relaxed (default)", "Organizational domain match (sub.example.com aligns with example.com)")
    pdf.bold_bullet("Strict", "Exact domain match required")

    # =========================================================================
    # 9. TLS & SECURITY
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("9", "TLS & Security")

    pdf.section_title("TLS Modes")
    pdf.bold_bullet("starttls", "Client connects in plaintext, then upgrades to TLS via STARTTLS command. Used on ports 25 and 587.")
    pdf.bold_bullet("implicit", "TLS from the first byte. Used on port 465 (SMTPS).")
    pdf.bold_bullet("none", "No TLS. Not recommended for production.")

    pdf.section_title("Certificate Management")
    pdf.body_text(
        "SendQ-MTA auto-generates a self-signed 'snakeoil' certificate on first start "
        "if no certificate is configured. For production, replace with a trusted certificate "
        "from Let's Encrypt or a commercial CA."
    )
    pdf.sub_section("Using Let's Encrypt")
    pdf.code_block(
        "# Install certbot\n"
        "apt install certbot\n"
        "\n"
        "# Obtain certificate\n"
        "certbot certonly --standalone -d mail.yourdomain.com\n"
        "\n"
        "# Update config:\n"
        "tls:\n"
        '  cert_file: "/etc/letsencrypt/live/mail.yourdomain.com/fullchain.pem"\n'
        '  key_file: "/etc/letsencrypt/live/mail.yourdomain.com/privkey.pem"\n'
        "\n"
        "# Reload\n"
        "sendq-mta reload"
    )

    pdf.section_title("Authentication Security")
    pdf.body_text(
        "SMTP authentication is supported via PLAIN and LOGIN mechanisms. "
        "Authentication is required on submission (port 587) and SMTPS (port 465) "
        "by default. Port 25 does not require auth for receiving inbound mail."
    )
    pdf.warning_box("Always use TLS when authentication is required to prevent credential exposure.")

    pdf.section_title("Open Relay Protection")
    pdf.body_text(
        "SendQ-MTA prevents open relay abuse. Mail is only accepted for relay if:\n"
        "- The recipient domain is a local domain, OR\n"
        "- The recipient domain is a configured relay domain, OR\n"
        "- The client is authenticated, OR\n"
        "- The client IP is in the trusted_networks list"
    )

    # =========================================================================
    # 10. RATE LIMITING
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("10", "Rate Limiting")
    pdf.body_text(
        "SendQ-MTA includes a multi-tier rate limiting engine to protect against abuse, "
        "spam, and resource exhaustion."
    )

    pdf.section_title("Inbound Rate Limits")
    pdf.bold_bullet("Per-IP connections", "Max 50 simultaneous connections from one IP.")
    pdf.bold_bullet("Per-IP messages", "Max 100 messages per IP per minute.")
    pdf.bold_bullet("Recipients per message", "Max 500 recipients per single message.")
    pdf.bold_bullet("Error threshold", "10 errors from an IP triggers automatic 1-hour ban.")

    pdf.section_title("Outbound Rate Limits")
    pdf.bold_bullet("Per-domain", "Max 200 messages per destination domain per minute.")
    pdf.bold_bullet("Global throughput", "Max 500 messages per second (token bucket algorithm).")

    pdf.section_title("Per-User Rate Limits")
    pdf.bold_bullet("Messages per hour", "Max 500 messages per authenticated user per hour.")
    pdf.bold_bullet("Recipients per hour", "Max 2000 recipients per authenticated user per hour.")

    pdf.section_title("Automatic IP Banning")
    pdf.body_text(
        "When a client IP exceeds the error threshold (default: 10 errors in 1 hour), "
        "it is automatically banned for the configured duration (default: 1 hour). "
        "Bans are tracked in memory and automatically expire."
    )

    # =========================================================================
    # 11. RELAY & DELIVERY
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("11", "Relay & Delivery")

    pdf.section_title("Direct MX Delivery (Default)")
    pdf.body_text(
        "When relay is disabled (default), SendQ-MTA delivers directly to recipient "
        "mail servers by looking up MX records via DNS. For each recipient domain:"
    )
    pdf.bullet("DNS MX lookup is performed for the recipient domain")
    pdf.bullet("MX hosts are tried in priority order (lowest preference first)")
    pdf.bullet("Opportunistic STARTTLS is used when available")
    pdf.bullet("If all MX hosts fail, the message is deferred for retry")
    pdf.ln(2)
    pdf.warning_box("Direct MX delivery requires a clean IP, valid PTR record, and proper HELO hostname.")

    pdf.section_title("Relay (Smarthost) Mode")
    pdf.body_text(
        "For servers behind NAT, shared hosting, or IP reputation issues, "
        "use an SMTP relay (smarthost) like Mailgun, SendGrid, Amazon SES, etc."
    )
    pdf.code_block(
        "relay:\n"
        "  enabled: true\n"
        '  host: "smtp.mailgun.org"\n'
        "  port: 587\n"
        '  username: "postmaster@yourdomain.com"\n'
        '  password: "your-api-key"\n'
        '  tls_mode: "starttls"\n'
        "  tls_verify: true"
    )

    pdf.section_title("Failover Relays")
    pdf.body_text("Configure backup relay servers for high availability:")
    pdf.code_block(
        "relay:\n"
        "  enabled: true\n"
        '  host: "primary-relay.example.com"\n'
        "  port: 587\n"
        "  failover:\n"
        '    - host: "backup-relay.example.com"\n'
        "      port: 587\n"
        '      username: "user"\n'
        '      password: "pass"\n'
        '      tls_mode: "starttls"'
    )

    pdf.section_title("Connection Pooling")
    pdf.body_text(
        "For high-volume delivery, SendQ-MTA maintains a pool of persistent SMTP connections:"
    )
    pdf.bold_bullet("Per-domain pool size", "10 connections per destination domain")
    pdf.bold_bullet("Total pool size", "500 connections maximum")
    pdf.bold_bullet("Idle timeout", "300 seconds before closing idle connections")
    pdf.bold_bullet("Max lifetime", "1800 seconds maximum connection age")
    pdf.bold_bullet("Health checking", "Connections validated with NOOP before reuse")

    # =========================================================================
    # 12. LOGGING & MONITORING
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("12", "Logging & Monitoring")

    pdf.section_title("Log Files")
    pdf.body_text("Default log location: /var/log/sendq-mta/sendq-mta.log")
    pdf.body_text("Logs are rotated automatically at 100 MB, with 30 files retained.")

    pdf.section_title("Log Formats")
    pdf.sub_section("JSON Format (Default)")
    pdf.code_block(
        '{"timestamp": "2026-02-27T04:11:15.521Z",\n'
        ' "level": "info",\n'
        ' "logger": "sendq-mta.queue",\n'
        ' "message": "Enqueued sendq-abc123 from=user@ex.com rcpts=1"}'
    )
    pdf.sub_section("Text Format")
    pdf.code_block(
        "2026-02-27 04:11:15 [INFO   ] sendq-mta.queue: Enqueued sendq-abc123"
    )

    pdf.section_title("Log Levels")
    pdf.bold_bullet("debug", "Verbose output for development. Includes SMTP protocol details.")
    pdf.bold_bullet("info", "Normal operation. Enqueue, deliver, defer, fail events.")
    pdf.bold_bullet("warning", "Connection errors, rate limit hits, delivery issues.")
    pdf.bold_bullet("error", "Fatal errors, all MX hosts failed, configuration problems.")

    pdf.section_title("Prometheus Metrics")
    pdf.body_text("Built-in Prometheus exporter at http://127.0.0.1:9225/metrics")
    pdf.body_text("Available metrics:")
    pdf.bullet("sendq_messages_received_total, sendq_messages_delivered_total")
    pdf.bullet("sendq_messages_deferred_total, sendq_messages_failed_total")
    pdf.bullet("sendq_queue_active, sendq_queue_deferred, sendq_queue_failed (gauges)")
    pdf.bullet("sendq_connections_inbound_total, sendq_connections_outbound_total")
    pdf.bullet("sendq_auth_success_total, sendq_auth_failure_total")
    pdf.bullet("sendq_tls_connections_total, sendq_rate_limited_total")
    pdf.bullet("sendq_uptime_seconds, sendq_delivery_workers_busy")

    pdf.section_title("Viewing Logs in Real-Time")
    pdf.code_block(
        "# Follow log output\n"
        "tail -f /var/log/sendq-mta/sendq-mta.log\n"
        "\n"
        "# Filter for errors only (JSON format)\n"
        'tail -f /var/log/sendq-mta/sendq-mta.log | grep \'"level": "error"\'\n'
        "\n"
        "# Systemd journal\n"
        "journalctl -u sendq-mta -f"
    )

    # =========================================================================
    # 13. ARCHITECTURE & DEVELOPER GUIDE
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("13", "Architecture & Developer Guide")

    pdf.section_title("Source Code Layout")
    pdf.code_block(
        "src/sendq_mta/\n"
        "  cli/main.py           # Click CLI -- all commands (1077 lines)\n"
        "  core/server.py        # Main SMTP server, listeners, signal handling\n"
        "  core/config.py        # YAML config loader, validator, hot-reload\n"
        "  core/rate_limiter.py  # Token bucket + sliding window rate limiter\n"
        "  core/management.py    # Management API (UNIX socket)\n"
        "  core/metrics.py       # Prometheus metrics collector\n"
        "  auth/authenticator.py # User CRUD, password hashing, authentication\n"
        "  auth/dkim.py          # DKIM signing and verification\n"
        "  auth/spf.py           # SPF checking\n"
        "  auth/dmarc.py         # DMARC policy enforcement\n"
        "  queue/manager.py      # Persistent queue, delivery workers, deferred scanner\n"
        "  transport/delivery.py # Relay and direct MX delivery engine\n"
        "  transport/connection_pool.py  # Connection pooling for outbound SMTP\n"
        "  utils/logging_setup.py       # Structured logging setup"
    )

    pdf.section_title("Threading Model")
    pdf.body_text(
        "SendQ-MTA is fully asynchronous, built on Python asyncio (3.11+):\n"
        "- aiosmtpd handles inbound SMTP protocol\n"
        "- aiosmtplib handles outbound SMTP connections\n"
        "- asyncio.Queue distributes messages to delivery workers\n"
        "- Background tasks: deferred scanner, metrics, connection pool cleanup\n"
        "- One daemon thread: rate limiter cleanup (runs every 5 minutes)"
    )

    pdf.section_title("Message Flow (Internal)")
    pdf.code_block(
        "Client --SMTP--> [aiosmtpd Listener]\n"
        "                       |\n"
        "                 [SendQHandler]\n"
        "                   - Rate limit check\n"
        "                   - Auth check\n"
        "                   - SPF/DMARC check\n"
        "                   - Domain policy check\n"
        "                       |\n"
        "                 [QueueManager.enqueue()]\n"
        "                   - Write .meta.json + .eml to disk\n"
        "                   - Push to asyncio.Queue\n"
        "                       |\n"
        "                 [_delivery_worker] (x16)\n"
        "                   - Pull from asyncio.Queue\n"
        "                   - DKIM sign (if enabled)\n"
        "                       |\n"
        "                 [DeliveryEngine.deliver()]\n"
        "                   - Relay mode OR MX lookup\n"
        "                   - Connect, TLS, AUTH, send\n"
        "                       |\n"
        "                 Success: delete from disk\n"
        "                 Failure: move to deferred/failed"
    )

    pdf.section_title("Running Tests")
    pdf.code_block(
        "# Install dev dependencies\n"
        "pip install -e '.[dev]'\n"
        "\n"
        "# Run all tests\n"
        "pytest tests/\n"
        "\n"
        "# Run with coverage\n"
        "pytest tests/ --cov=src/sendq_mta --cov-report=term-missing\n"
        "\n"
        "# Run specific test file\n"
        "pytest tests/test_auth.py -v\n"
        "\n"
        "# Type checking\n"
        "mypy src/sendq_mta/\n"
        "\n"
        "# Linting\n"
        "ruff check src/"
    )

    pdf.section_title("Key Dependencies")
    pdf.bold_bullet("aiosmtpd >= 1.4.6", "Async SMTP server framework")
    pdf.bold_bullet("aiosmtplib >= 3.0.0", "Async SMTP client for outbound delivery")
    pdf.bold_bullet("pyyaml >= 6.0", "YAML configuration parsing")
    pdf.bold_bullet("click >= 8.1", "CLI framework")
    pdf.bold_bullet("dnspython >= 2.4", "DNS MX record lookups")
    pdf.bold_bullet("argon2-cffi >= 23.1", "Password hashing (primary)")
    pdf.bold_bullet("dkimpy >= 1.1.0", "DKIM signing/verification (optional)")
    pdf.bold_bullet("pyspf >= 2.0.14", "SPF checking (optional)")
    pdf.bold_bullet("cryptography >= 41.0", "DKIM key generation (optional)")

    # =========================================================================
    # 14. TROUBLESHOOTING
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("14", "Troubleshooting")

    # Issue 1
    pdf.section_title('Error: "Helo command rejected: need fully-qualified hostname"')
    pdf.body_text(
        "Remote servers reject your HELO/EHLO greeting because the hostname is not "
        "a fully-qualified domain name (e.g., just 'muscat' instead of 'mail.example.com')."
    )
    pdf.sub_section("Solution")
    pdf.body_text("Set a proper FQDN in /etc/sendq-mta/sendq-mta.yml:")
    pdf.code_block('server:\n  hostname: "mail.yourdomain.com"')
    pdf.body_text("Also set the system hostname:")
    pdf.code_block("hostnamectl set-hostname mail.yourdomain.com")
    pdf.body_text("Ensure the FQDN has a matching A record and PTR (reverse DNS) record.")

    # Issue 2
    pdf.section_title("Server Shows STOPPED After flush-queue")
    pdf.body_text(
        "In older versions, flush-queue sent SIGUSR1 without a registered handler, "
        "which terminated the server process. This has been fixed. If you encounter this, "
        "update to the latest version."
    )
    pdf.sub_section("Solution")
    pdf.code_block("# Update and restart\ngit pull && pip install -e .\nsudo systemctl restart sendq-mta")

    # Issue 3
    pdf.section_title("All MX Hosts Failed for Domain")
    pdf.body_text(
        "SendQ-MTA tried all MX servers for the destination domain and all rejected "
        "the message or were unreachable."
    )
    pdf.sub_section("Common Causes")
    pdf.bullet("Incorrect HELO hostname (see above)")
    pdf.bullet("IP address is blacklisted (check at mxtoolbox.com/blacklists)")
    pdf.bullet("No PTR (reverse DNS) record for your server IP")
    pdf.bullet("Missing or incorrect SPF record for your sending domain")
    pdf.bullet("Firewall blocking outbound port 25")
    pdf.bullet("Self-signed TLS certificate rejected by remote server")

    # Issue 4
    pdf.section_title("Permission Denied on /etc/sendq-mta")
    pdf.body_text("The sendq user cannot read configuration files.")
    pdf.sub_section("Solution")
    pdf.code_block(
        "sudo chown -R sendq:sendq /etc/sendq-mta\n"
        "sudo chmod 750 /etc/sendq-mta\n"
        "sudo chmod 640 /etc/sendq-mta/sendq-mta.yml\n"
        "sudo chmod 600 /etc/sendq-mta/users.yml"
    )

    # Issue 5
    pdf.section_title("Cannot Bind to Port 25 (Permission Denied)")
    pdf.body_text("Ports below 1024 require special privileges.")
    pdf.sub_section("Solution")
    pdf.body_text("If using systemd, the service unit already grants CAP_NET_BIND_SERVICE. "
                   "If running manually:")
    pdf.code_block("sudo setcap 'cap_net_bind_service=+ep' $(which python3)")

    # Issue 6
    pdf.section_title("Messages Stuck in Deferred Queue")
    pdf.body_text("Messages keep retrying and never deliver.")
    pdf.sub_section("Diagnosis")
    pdf.code_block(
        "# View deferred messages with details\n"
        "sendq-mta queue-status -v\n"
        "\n"
        "# Check the last error for each message\n"
        "cat /var/spool/sendq-mta/deferred/*.meta.json | python3 -m json.tool\n"
        "\n"
        "# Check logs for the specific message ID\n"
        "grep 'sendq-abc123' /var/log/sendq-mta/sendq-mta.log"
    )

    # Issue 7
    pdf.section_title("SSL/TLS Certificate Errors")
    pdf.body_text("Errors related to TLS handshake or certificate verification.")
    pdf.sub_section("Solution")
    pdf.body_text("1. Verify your certificate files are readable:")
    pdf.code_block("openssl x509 -in /etc/sendq-mta/certs/snakeoil.pem -text -noout")
    pdf.body_text("2. For relay TLS verification failures with self-signed certs:")
    pdf.code_block("relay:\n  tls_verify: false    # Only for testing!")

    # Issue 8
    pdf.section_title("Rate Limited / IP Banned")
    pdf.body_text("Your test client gets rejected with rate limit errors.")
    pdf.sub_section("Solution")
    pdf.body_text("Temporarily increase limits or disable rate limiting for testing:")
    pdf.code_block(
        "rate_limiting:\n"
        "  enabled: false    # Disable for testing only"
    )

    # Issue 9
    pdf.section_title("Service Fails to Start (Systemd)")
    pdf.sub_section("Diagnosis")
    pdf.code_block(
        "sudo systemctl status sendq-mta\n"
        "sudo journalctl -u sendq-mta -e --no-pager\n"
        "\n"
        "# Validate configuration\n"
        "sendq-mta validate-config\n"
        "\n"
        "# Try foreground mode for full error output\n"
        "sendq-mta start -f"
    )

    # Issue 10
    pdf.section_title("Authentication Failures")
    pdf.body_text("Users cannot authenticate via SMTP.")
    pdf.sub_section("Checklist")
    pdf.bullet("Verify user exists: sendq-mta show-user <username>")
    pdf.bullet("Verify user is enabled: sendq-mta edit-user <username> --enable")
    pdf.bullet("Test password: sendq-mta change-pass <username>")
    pdf.bullet("Check listener requires auth: require_auth must be true on port 587/465")
    pdf.bullet("Ensure TLS is working (AUTH over plaintext is insecure and may be rejected)")

    # Issue 11
    pdf.section_title("Relay Connection Failures")
    pdf.sub_section("Diagnosis")
    pdf.code_block(
        "# Test relay connectivity\n"
        "sendq-mta test-relay\n"
        "\n"
        "# Manual test with openssl\n"
        "openssl s_client -connect smtp.relay.com:587 -starttls smtp"
    )
    pdf.body_text("Common causes: wrong credentials, firewall blocking port, TLS mode mismatch.")

    # =========================================================================
    # 15. FAQ
    # =========================================================================
    pdf.add_page()
    pdf.chapter_title("15", "Frequently Asked Questions (FAQ)")

    faqs = [
        (
            "What ports does SendQ-MTA listen on?",
            "By default: port 25 (SMTP), port 587 (Submission), and port 465 (SMTPS). "
            "Port 25 is for receiving inbound mail (no auth required). "
            "Ports 587 and 465 are for authenticated submission from mail clients."
        ),
        (
            "Do I need a relay, or can I send directly?",
            "SendQ-MTA supports both modes. Direct MX delivery works if your server "
            "has a clean IP address, valid PTR record, and is not on any blacklists. "
            "If your IP is shared or has reputation issues, use a relay (smarthost) "
            "like Mailgun, SendGrid, or Amazon SES."
        ),
        (
            "How do I send a test email?",
            "Use the built-in test command:\n"
            "  sendq-mta test-send --to recipient@example.com\n"
            "This sends a test message through your local MTA and reports success or failure."
        ),
        (
            "How do I check if my server is an open relay?",
            "SendQ-MTA prevents open relay by default. Only authenticated users, trusted "
            "networks, and mail to local/relay domains are accepted. You can verify with:\n"
            "  telnet your-server 25\n"
            "  EHLO test\n"
            "  MAIL FROM:<test@external.com>\n"
            "  RCPT TO:<test@other-external.com>\n"
            "This should be rejected with '550 Relay denied'."
        ),
        (
            "Can I use Let's Encrypt certificates?",
            "Yes. Obtain a certificate with certbot, then update the tls.cert_file and "
            "tls.key_file paths in sendq-mta.yml to point to the Let's Encrypt files. "
            "Run 'sendq-mta reload' to apply without downtime. Set up a certbot renewal "
            "hook to reload SendQ-MTA after each renewal."
        ),
        (
            "How do I monitor SendQ-MTA?",
            "Built-in Prometheus metrics exporter at http://127.0.0.1:9225/metrics. "
            "Connect it to Grafana for dashboards. Also check logs at "
            "/var/log/sendq-mta/sendq-mta.log and use 'sendq-mta status' for quick checks."
        ),
        (
            "What is the maximum message size?",
            "Default: 50 MB (52428800 bytes). Configure with server.max_message_size in the "
            "YAML config. Set to 0 for no limit (not recommended)."
        ),
        (
            "How does hot-reload work?",
            "Send SIGHUP to the server process or run 'sendq-mta reload'. The configuration "
            "file is re-read from disk and settings are applied without restarting. "
            "Note: Listener ports cannot be changed without a full restart."
        ),
        (
            "What happens to messages if the server crashes?",
            "Messages are persisted to disk immediately on receipt. When the server restarts, "
            "it automatically loads all messages from the active queue directory and resumes "
            "delivery. No messages are lost."
        ),
        (
            "How do I back up the message queue?",
            "The queue is stored as files in /var/spool/sendq-mta/. Back up the queue/, "
            "deferred/, and failed/ directories. Each message is two files: .meta.json "
            "(metadata) and .eml (message body)."
        ),
        (
            "Can I run multiple instances?",
            "Yes, by using separate config files with different PID files, queue directories, "
            "and listener ports. Start each with: sendq-mta -c /path/to/config.yml start"
        ),
        (
            "What Python version is required?",
            "Python 3.11 or later. SendQ-MTA uses modern async features and type hints "
            "that require 3.11+. Tested on Python 3.11, 3.12, and 3.13."
        ),
        (
            "How do I completely uninstall SendQ-MTA?",
            "Run the uninstall script:\n"
            "  sudo bash scripts/uninstall.sh\n"
            "This removes the package, virtualenv, systemd service, and optionally "
            "the configuration and queue directories."
        ),
        (
            "Why are my emails going to spam?",
            "Common reasons: (1) No SPF record for your domain, (2) No DKIM signing enabled, "
            "(3) No DMARC record, (4) Missing or incorrect PTR record, (5) IP is on a "
            "blacklist, (6) Server hostname doesn't match PTR. Set up all DNS records "
            "(see Section 2) and enable DKIM signing (see Section 8)."
        ),
        (
            "How do I increase delivery throughput?",
            "Increase queue workers (queue.workers), connection pool sizes, and outbound "
            "rate limits. Default 16 workers handle most workloads. For high volume, "
            "increase to 32-64 workers and adjust rate limits accordingly."
        ),
    ]

    for q, a in faqs:
        pdf.set_font(SANS, "B", 11)
        pdf.set_text_color(25, 60, 120)
        pdf.cell(0, 7, f"Q: {q}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font(SANS, "", 10)
        pdf.set_text_color(40, 40, 40)
        pdf.multi_cell(0, 5.5, f"A: {a}")
        pdf.ln(4)

    # =========================================================================
    # OUTPUT
    # =========================================================================
    output_path = "/home/user/mta-mask/SendQ-MTA_Documentation.pdf"
    pdf.output(output_path)
    print(f"Documentation generated: {output_path}")
    return output_path


if __name__ == "__main__":
    build_pdf()
