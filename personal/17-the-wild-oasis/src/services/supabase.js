import { createClient } from "@supabase/supabase-js";

export const supabaseUrl = "https://djhsunknokbjqboxfzjl.supabase.co";
const supabaseKey =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqaHN1bmtub2tianFib3hmempsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk3NzcxMjQsImV4cCI6MjA5NTM1MzEyNH0.zI9hTXJ8x4H78LCDfSwVCTcitBgkuAWgk13lwVJcWBg";
const supabase = createClient(supabaseUrl, supabaseKey);

export default supabase;
