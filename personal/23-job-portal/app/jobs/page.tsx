"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { getJobs } from "../services/auth";
import { getToken, logout } from "../services/authHelper";

type Job = {
  id: string | number;
  title: string;
  description: string;
};

function Jobs() {
  const router = useRouter();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    let isActive = true;

    async function loadJobs() {
      const token = getToken();

      if (!token) {
        if (isActive) {
          setJobs([]);
          setError("");
          setIsLoggedIn(false);
          setLoading(false);
        }
        return;
      }

      try {
        setJobs([]);
        setError("");
        const data = await getJobs(token);

        if (isActive) {
          setJobs(data);
          setIsLoggedIn(true);
        }
      } catch (err) {
        if (isActive) {
          setError(err instanceof Error ? err.message : "Failed to load jobs");
        }
      } finally {
        if (isActive) {
          setLoading(false);
        }
      }
    }

    loadJobs();

    return () => {
      isActive = false;
    };
  }, []);

  function handleLogout() {
    logout();
    setJobs([]);
    setError("");
    setIsLoggedIn(false);
    setLoading(false);
    router.replace("/login");
  }

  if (loading) {
    return (
      <div className="page-shell">
        <h1>Jobs</h1>
        <p>Loading jobs...</p>
      </div>
    );
  }

  if (!isLoggedIn) {
    return (
      <div className="page-shell">
        <h1>Jobs</h1>
        <p>You are not logged in</p>
      </div>
    );
  }

  return (
    <main className="page-shell">
      <div className="page-header">
        <div>
          <h1>Jobs</h1>
          <p>Manage your posted jobs.</p>
        </div>
        <div className="actions">
          <Link className="button primary" href="/jobs/create">
            Create Job
          </Link>
          <button className="button" type="button" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>

      {error ? <p className="message error">{error}</p> : null}
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Description</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {jobs.map((job) => (
            <tr key={job.id}>
              <td>{job.id}</td>
              <td>
                <Link href={`/jobs/${job.id}`}>{job.title}</Link>
              </td>
              <td>{job.description}</td>
              <td>
                <Link href={`/jobs/${job.id}`}>View</Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}

export default Jobs;
