/* eslint-disable no-console */
import { QueryClient } from "@tanstack/react-query";
import _ from "lodash";
import { useEffect, useState } from "react";

export async function openSocket() {
  const url = new URL(
    "/ws/notifications",
    window.location.origin.replace("https", "wss")
  );

  return new Promise<WebSocket>((resolve, reject) => {
    const socket = new WebSocket(url.toString());

    socket.onopen = () => {
      resolve(socket);
    };

    socket.onerror = (error) => {
      reject(error);
    };
  });
}

export type Notification = {
  id: string;
  task_id: string;
  task_name: string | null;
  task_status: string;
  extras: Record<string, string>;
};

export type WSMessage = {
  type: string;
  notification: {
    id: string;
    user_id: number;
    resource_id: string;
    resource: "playlist" | "album";
    operation: "sync" | "analyze";
    task_id: string;
    task_name: string | null;
    task_status: string;
    extras: string | Record<string, string>;
    created_at: string;
    updated_at: string;
  };
};

export function useNotifications(client: QueryClient) {
  const [isConnected, setIsConnected] = useState(false);
  useEffect(() => {
    const socket = new WebSocket(
      new URL(
        "/ws/notifications",
        window.location.origin.replace("https", "wss")
      )
    );
    const queryKey = ["pushNotification"];

    socket.onopen = () => {
      console.debug("Socket opened");

      setIsConnected(true);
    };

    socket.onmessage = (event: MessageEvent<string>) => {
      try {
        const message: WSMessage = JSON.parse(event.data);

        client.setQueryData(queryKey, () => message);
        console.debug("Received message", message);

        if (
          message.notification.resource === "playlist" &&
          message.type === "task_complete" &&
          message.notification.operation === "analyze"
        ) {
          console.debug("Invalidating query", message);
          client.invalidateQueries({
            queryKey: [
              "browser",
              "playlists",
              message.notification.resource_id,
            ],
          });
        }
      } catch (error) {
        console.error("Error parsing message", error);

        setIsConnected(false);
      }
    };

    socket.onclose = () => {
      console.debug("Socket closed");

      setIsConnected(false);
    };
  }, [client]);

  return { isConnected };
}
