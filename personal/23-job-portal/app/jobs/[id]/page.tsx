"use client";

import { use, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getJob } from "../../services/auth";
import { getToken } from "../../services/authHelper";

type Job = {
  id: string | number;
  title: string;
  description: string;
};

type JobDetailsPageProps = {
  params: Promise<{
    id: string;
  }>;
};

export default function JobDetailsPage({ params }: JobDetailsPageProps) {
  const router = useRouter();
  const { id } = use(params);
  const [job, setJob] = useState<Job | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let isActive = true;

    async function loadJob() {
      const token = getToken();

      if (!token) {
        if (isActive) {
          setError("You are not logged in");
          setLoading(false);
        }
        return;
      }

      try {
        setError("");
        const data = await getJob(token, id);

        if (isActive) {
          setJob(data);
        }
      } catch (err) {
        if (isActive) {
          setError(err instanceof Error ? err.message : "Failed to load job");
        }
      } finally {
        if (isActive) {
          setLoading(false);
        }
      }
    }

    loadJob();

    return () => {
      isActive = false;
    };
  }, [id]);

  return (
    <main className="page-shell">
      <div className="page-header">
        <div>
          <h1>Job Details</h1>
          <p>Review this job posting.</p>
        </div>
        <button
          className="button"
          type="button"
          onClick={() => router.push("/jobs")}
        >
          Back
        </button>
      </div>

      {loading ? <p>Loading job...</p> : null}
      {error ? <p className="message error">{error}</p> : null}
      {job ? (
        <div className="detail-card">
          <p>Job ID: {job.id}</p>
          <h2>{job.title}</h2>
          <p>{job.description}</p>
        </div>
      ) : null}
    </main>
  );
}
