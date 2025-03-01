"use client"

import { TableHeader } from "@/components/ui/table"
import type React from "react"
import { useState } from "react"
import { Copy, ExternalLink, LinkIcon, Loader2, Moon, Sun } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Toaster } from "@/components/ui/toaster"
import { useToast } from "@/components/ui/use-toast"
import { Card, CardContent } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableRow } from "@/components/ui/table"
import Link from "next/link"
import { useTheme } from "@/lib/theme-provider"
import { useMutation } from "@tanstack/react-query"
import { shortenUrl, type ShortenedUrl } from "@/lib/api"

interface UrlShortenerState {
  urls: ShortenedUrl[];
  url: string;
  autoFill: boolean;
}

export default function UrlShortener() {
  const [state, setState] = useState<UrlShortenerState>({
    urls: [],
    url: "",
    autoFill: false,
  });
  const { toast } = useToast();
  const { theme, setTheme } = useTheme();

  const shortenUrlMutation = useMutation({
    mutationFn: (url: string) => shortenUrl({ target_url: url }),
    onSuccess: (data) => {
      setState((prev) => ({
        ...prev,
        urls: [data, ...prev.urls],
        url: "",
      }));
      toast({
        title: "URL shortened successfully!",
        description: "Your shortened URL is ready to use.",
      });
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: "Failed to shorten URL. Please try again.",
        variant: "destructive",
      });
    },
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!state.url) {
      toast({
        title: "Error",
        description: "Please enter a URL to shorten",
        variant: "destructive",
      });
      return;
    }

    shortenUrlMutation.mutate(state.url);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast({
      title: "Copied to clipboard",
      description: "The shortened URL has been copied to your clipboard.",
    });
  };

  const handleAutoFillChange = (checked: boolean) => {
    setState((prev) => ({ ...prev, autoFill: checked }));
    if (checked) {
      navigator.clipboard
        .readText()
        .then((clipText) => {
          if (clipText && clipText.startsWith("http")) {
            setState((prev) => ({ ...prev, url: clipText }));
          }
        })
        .catch((err) => {
          console.error("Failed to read clipboard: ", err);
        });
    }
  };

  return (
    <div className="flex min-h-screen flex-col bg-white dark:bg-slate-950 text-slate-900 dark:text-white">
      <header className="container mx-auto flex items-center justify-between py-6">
        <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
          <LinkIcon className="h-6 w-6 text-pink-500" />
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-500 to-pink-500 bg-clip-text text-transparent">
            Shortify
          </h1>
        </Link>
        <div className="flex gap-4 items-center">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setTheme(theme === "light" ? "dark" : "light")}
          >
            {theme === "light" ? <Moon className="h-5 w-5" /> : <Sun className="h-5 w-5" />}
          </Button>
          <Button
            variant="outline"
            className="border-slate-700 dark:text-white hover:bg-slate-800 dark:hover:bg-slate-800 hover:text-white"
          >
            Login
          </Button>
          <Button className="bg-blue-600 hover:bg-blue-700">Register Now</Button>
        </div>
      </header>

      <main className="container mx-auto flex-1 px-4 py-8">
        <div className="mx-auto max-w-3xl text-center">
          <h2 className="mb-4 text-4xl font-bold md:text-5xl">
            <span className="text-blue-500">Shorten</span> <span className="text-pink-500">Your</span>{" "}
            <span className="text-blue-500">Loooong</span> <span className="text-pink-500">Links</span>{" "}
            <span className="text-blue-500">:)</span>
          </h2>
          <p className="mb-8 text-slate-600 dark:text-slate-400">
            Shortify is an efficient and easy-to-use URL shortening service that streamlines your online experience.
          </p>

          <Card className="bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-800">
            <CardContent className="pt-6">
              <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                <div className="relative">
                  <div className="absolute left-3 top-3 text-slate-400 dark:text-slate-400">
                    <LinkIcon className="h-5 w-5" />
                  </div>
                  <Input
                    type="url"
                    placeholder="Enter the link here"
                    value={state.url}
                    onChange={(e) => setState((prev) => ({ ...prev, url: e.target.value }))}
                    className="pl-10 bg-white dark:bg-slate-800 border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white h-12 focus-visible:ring-blue-500"
                  />
                  <Button
                    type="submit"
                    className="absolute right-0 top-0 h-12 bg-blue-600 hover:bg-blue-700 rounded-l-none"
                    disabled={shortenUrlMutation.isPending}
                  >
                    {shortenUrlMutation.isPending ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Shortening...
                      </>
                    ) : (
                      "Shorten Now!"
                    )}
                  </Button>
                </div>

                <div className="flex items-center justify-center space-x-2">
                  <Switch id="auto-fill" checked={state.autoFill} onCheckedChange={handleAutoFillChange} />
                  <Label htmlFor="auto-fill" className="text-slate-400 dark:text-slate-400">
                    Auto Paste from Clipboard
                  </Label>
                </div>
              </form>
            </CardContent>
          </Card>

          {state.urls.length > 0 && (
            <div className="mt-8">
              <Card className="bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-800">
                <CardContent className="pt-6">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Original URL</TableHead>
                        <TableHead>Short URL</TableHead>
                        <TableHead>Clicks</TableHead>
                        <TableHead>Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {state.urls.map((item) => (
                        <TableRow key={item.id}>
                          <TableCell className="font-medium max-w-[200px] truncate">
                            {item.target_url}
                          </TableCell>
                          <TableCell>{item.short_code}</TableCell>
                          <TableCell>{item.clicks}</TableCell>
                          <TableCell>
                            <div className="flex gap-2">
                              <Button
                                variant="ghost"
                                size="icon"
                                onClick={() => copyToClipboard(item.short_code)}
                              >
                                <Copy className="h-4 w-4" />
                              </Button>
                              <Button
                                variant="ghost"
                                size="icon"
                                asChild
                              >
                                <Link href={item.short_code} target="_blank">
                                  <ExternalLink className="h-4 w-4" />
                                </Link>
                              </Button>
                            </div>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </main>
      <Toaster />
    </div>
  );
}

