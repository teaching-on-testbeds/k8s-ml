all: reserve_fabric.ipynb delete_fabric.ipynb

clean:
	rm reserve_fabric.ipynb delete_fabric.ipynb

CUSTDIR := custom-snippets
SNIPDIR := ../fabric-snippets
SNIPPETS := $(SNIPDIR)/fab-config.md $(SNIPDIR)/configure-resources.md $(SNIPDIR)/draw-topo-detailed-labels.md 
reserve_fabric.ipynb: $(SNIPPETS) $(CUSTDIR)/intro.md $(CUSTDIR)/exp-def.md $(CUSTDIR)/exp-kubespray.md $(CUSTDIR)/reserve-resources.md
	pandoc --wrap=none \
                -i $(CUSTDIR)/intro.md \
				$(SNIPDIR)/fab-config.md \
				$(CUSTDIR)/exp-def.md \
				$(CUSTDIR)/reserve-resources.md \
				$(SNIPDIR)/configure-resources.md \
				$(SNIPDIR)/draw-topo-detailed-labels.md \
				$(CUSTDIR)/exp-kubespray.md \
                -o reserve_fabric.ipynb  

SNIPPETS := $(SNIPDIR)/fab-config.md $(SNIPDIR)/delete-slice.md 
delete_fabric.ipynb: $(SNIPPETS) $(CUSTDIR)/intro-delete.md $(CUSTDIR)/exp-def.md 
	pandoc --wrap=none \
                -i $(CUSTDIR)/intro-delete.md \
				$(SNIPDIR)/fab-config.md \
				$(CUSTDIR)/exp-def.md \
				$(SNIPDIR)/delete-slice.md \
                -o delete_fabric.ipynb  
