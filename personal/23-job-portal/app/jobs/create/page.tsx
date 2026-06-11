"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { createJob } from "../../services/auth";
import { getToken } from "../../services/authHelper";

export default function CreateJobPage() {
  const router = useRouter();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const token = getToken();

    if (!token) {
      router.replace("/login");
      return;
    }

    try {
      setSubmitting(true);
      setError("");
      await createJob(token, title, description);
      router.push("/jobs");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create job");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="page-shell">
      <div className="page-header">
        <div>
          <h1>Create Job</h1>
          <p>Add a new job for your employer account.</p>
        </div>
        <button
          className="button"
          type="button"
          onClick={() => router.push("/jobs")}
        >
          Back
        </button>
      </div>

      <form className="form-card" onSubmit={handleSubmit}>
        {error ? <p className="message error">{error}</p> : null}

        <label className="field">
          <span>Title</span>
          <input
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            required
            placeholder="Frontend Developer"
          />
        </label>

        <label className="field">
          <span>Description</span>
          <textarea
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            required
            rows={6}
            placeholder="Describe the role, responsibilities, and requirements."
          />
        </label>

        <div className="actions">
          <button
            className="button primary"
            type="submit"
            disabled={submitting}
          >
            {submitting ? "Creating..." : "Create Job"}
          </button>
        </div>
      </form>
    </main>
  );
}
