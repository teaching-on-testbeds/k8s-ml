all: reserve_chameleon.ipynb delete_chameleon.ipynb

clean:
	rm reserve_chameleon.ipynb delete_chameleon.ipynb

CUSTDIR := custom-snippets
SNIPDIR := ../chameleon-snippets
SNIPPETS := $(SNIPDIR)/chi-config.md $(SNIPDIR)/reserve-resources.md $(SNIPDIR)/configure-resources.md $(SNIPDIR)/draw-topo-detailed-labels.md 
reserve_chameleon.ipynb: $(SNIPPETS) $(CUSTDIR)/intro.md $(CUSTDIR)/exp-def.md $(CUSTDIR)/exp-config.md $(CUSTDIR)/exp-kubespray.md
	pandoc --wrap=none \
                -i $(CUSTDIR)/intro.md \
				$(SNIPDIR)/chi-config.md \
				$(CUSTDIR)/exp-def.md \
				$(CUSTDIR)/exp-config.md \
				$(SNIPDIR)/draw-topo-detailed-labels.md \
				$(CUSTDIR)/exp-kubespray.md \
                -o reserve_chameleon.ipynb  

SNIPPETS := $(SNIPDIR)/chi-config.md $(SNIPDIR)/delete-slice.md 
delete_chameleon.ipynb: $(SNIPPETS) $(CUSTDIR)/intro-delete.md $(CUSTDIR)/exp-def.md 
	pandoc --wrap=none \
                -i $(CUSTDIR)/intro-delete.md \
				$(SNIPDIR)/chi-config.md \
				$(CUSTDIR)/exp-def.md \
				$(SNIPDIR)/delete-slice.md \
                -o delete_chameleon.ipynb  
