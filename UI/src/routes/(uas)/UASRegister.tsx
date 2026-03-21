import React from "react";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/(uas)/UASRegister")({
  component: UASRegister,
});

function UASRegister() {
  return <div>UASRegister</div>;
}

export default UASRegister;
