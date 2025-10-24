import { useEffect } from "react";
import { authApi } from "@/api/auth";
import { useNavigate } from "react-router-dom";
import { useToast } from "@/hooks/use-toast";

// This component handles the Gmail OAuth callback
export default function GmailCallback() {
  const navigate = useNavigate();
  const { toast } = useToast();

  useEffect(() => {
    const url = new URL(window.location.href);
    const code = url.searchParams.get("code");
    if (code) {
      authApi
        .handleGmailCallback(code)
        .then(() => {
          toast({ title: "Gmail Connected!", description: "You can now sync your emails." });
          navigate("/dashboard");
        })
        .catch((err) => {
          toast({ title: "Gmail Auth Failed", description: err?.response?.data?.detail || String(err), variant: "destructive" });
          navigate("/dashboard");
        });
    } else {
      toast({ title: "No code in callback", description: "Gmail authorization failed.", variant: "destructive" });
      navigate("/dashboard");
    }
  }, [navigate, toast]);

  return <div>Connecting Gmail...</div>;
}
