load("@rules_go//go:def.bzl", "go_binary", "go_library")

go_library(
    name = "quote_lib",
    srcs = ["quote.go"],
    importpath = "gitlab.com/hooshi/DSA-practice/go_tutorial/cmd/quote",
    visibility = ["//visibility:private"],
    deps = ["@io_rsc_quote//:quote"],
)

go_binary(
    name = "quote",
    embed = [":quote_lib"],
    visibility = ["//visibility:public"],
)
