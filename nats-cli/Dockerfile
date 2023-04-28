FROM golang
RUN go install github.com/nats-io/natscli/nats@latest && nats context add nats --server nats:4222 --description "NATS Bifrost" --select
CMD "bash"
