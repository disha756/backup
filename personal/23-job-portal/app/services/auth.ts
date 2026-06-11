"use server";

import { redirect } from "next/navigation";

const API_URL = "http://127.0.0.1:8000";

export async function registerUser(
  // name: string,
  // email: string,
  // password: string,
  formData: FormData,
) {
  console.log(formData, typeof formData);
  const jsonData = Object.fromEntries(formData.entries());

  console.log(jsonData, typeof jsonData);
  // console.log(name, email, password);
  const response = await fetch(`${API_URL}/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(jsonData),
    // body: JSON.parse({
    //   ...formData,
    //   // formData.name,
    //   // formData.email,
    //   // formData.password,
    // }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Registration failed");
  }

  redirect("/login");
  // return data;
}

export async function login(email: string, password: string) {
  const response = await fetch(`${API_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Login failed");
  }

  // setToken(data.access_token);
  // redirect("/jobs");
  return data;
}

export async function getJobs(token: string) {
  // const token = localStorage.getItem("token");
  // const token = getToken();

  const response = await fetch(`${API_URL}/jobs`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    cache: "no-store",
  });

  const data = await response.json();
  console.log(data);

  if (!response.ok) {
    throw new Error(data.detail || "Login failed");
  }

  return data;
}

export async function getJob(token: string, id: string) {
  const response = await fetch(`${API_URL}/jobs/${id}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    cache: "no-store",
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to load job");
  }

  return data;
}

export async function createJob(
  token: string,
  title: string,
  description: string,
) {
  const response = await fetch(`${API_URL}/jobs`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ title, description }),
    cache: "no-store",
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to create job");
  }

  return data;
}
