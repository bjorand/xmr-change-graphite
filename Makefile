release:
	docker build -t bjorand/xmr-change-graphite .
	docker tag bjorand/xmr-change-graphite bjorand/xmr-change-graphite:latest
	docker push bjorand/xmr-change-graphite:latest
