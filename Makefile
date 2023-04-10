all: index.md 


index.md: prepare.md footer.md reserve/index.md deploy_app/index.md deploy_k8s/index.md deploy_lb/index.md deploy_hpa/index.md
	pandoc --resource-path=images/ --wrap=none \
                -i prepare.md \
		reserve/index.md deploy_app/index.md \
                deploy_k8s/index.md deploy_lb/index.md deploy_hpa/index.md \
                --metadata title="k8s-ml" -o index.tmp.md
	grep -v '^:::' index.tmp.md > index.md
	rm index.tmp.md
	cat footer.md >> index.md