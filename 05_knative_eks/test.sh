EXTERNAL_HOST=a1272037ff1374b489520a2f514ee2b4-1331222714.us-west-2.elb.amazonaws.com
SERVICE_HOSTNAME=cifar10.default.emlo.mmg
MODEL_NAME=cifar10
# curl -v \
# 	-H "Host: $SERVICE_HOSTNAME" \
# 	-H "Content-Type: application/json" \
# 	$EXTERNAL_HOST/v1/models/$MODEL_NAME:predict \
# 	-d @./input.json

hey -z 1s -c 1 -m POST -host ${SERVICE_HOSTNAME} -D ./input.json http://$EXTERNAL_HOST/v1/models/$MODEL_NAME:predict

