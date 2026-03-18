FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
ARG TARGET=worker
RUN CGO_ENABLED=0 go build -o /bin/app ./${TARGET}/main.go

FROM alpine:3.20
RUN apk --no-cache add ca-certificates
COPY --from=builder /bin/app /bin/app
ENTRYPOINT ["/bin/app"]
