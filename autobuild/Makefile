PKGCONFIG=pkg-config
UNITDIR=$(shell $(PKGCONFIG) systemd --variable=systemdsystemunitdir)
INSTDIR=/opt/paperbot

install:
	mkdir -p $(INSTDIR)
	cp -r * $(INSTDIR)
	git rev-parse HEAD > $(INSTDIR)/version
	install -Dm644 'paperbot.service' "$(UNITDIR)/paperbot.service"
	@echo "To enable paperbot: sudo systemctl enable paperbot"


