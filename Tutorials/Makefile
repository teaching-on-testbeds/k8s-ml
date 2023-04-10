all: index.md 


index.md: prepare.md footer.md notebooks/*.md
	pandoc --resource-path=images/ --wrap=none \
                -i prepare.md \
		notebooks/part0.md notebooks/part1.md \
                notebooks/part2.md notebooks/part3.md \
                --metadata title="k8s-ml" -o index.tmp.md
	grep -v '^:::' index.tmp.md > index.md
	rm index.tmp.md
	cat footer.md >> index.md