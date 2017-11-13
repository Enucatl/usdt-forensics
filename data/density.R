#!/usr/bin/env Rscript

library(argparse)
library(ggplot2)
library(data.table)
library(anytime)
library(scales)
library(zoo)

commandline_parser = ArgumentParser(description="plot usdt data")
commandline_parser$add_argument("links", nargs="?", default="links.csv")
args = commandline_parser$parse_args()

usdt = fread(args$links)
usdt[, date := anytime(timestamp, tz="UTC")]
setkey(usdt, "timestamp")
print(usdt)

plot = ggplot(usdt, aes(x=date, weight=value / 1e6)) +
    geom_histogram(binwidth=1200) +
    scale_x_datetime(date_breaks="12 hours") +
    xlab("time (UTC)") +
    ylab("transactions (MUSDT)") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))

print(plot)
width = 10
factor = 0.618
height = factor * width
ggsave("density.png", plot, width=width, height=height, dpi=300)
invisible(readLines("stdin", n=1))
