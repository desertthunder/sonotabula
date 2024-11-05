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

/**
 * {
    "id": "290a4810-4c80-409f-9ded-c9a33caffa18",
    "user_id": 1,
    "resource_id": "d6f0e40a-0070-467d-a8be-3572d22da077",
    "resource": "playlist",
    "operation": "sync",
    "task_id": "1a65d446-32b4-4108-85db-9bb11f50b4f2",
    "task_name": "sync_playlist",
    "task_status": "SUCCESS",
    "extras": "{\"playlist_id\": \"d6f0e40a-0070-467d-a8be-3572d22da077\", \"task_type\": \"sync_playlist\"}",
    "created_at": "2024-11-03T22:12:13.916063Z",
    "updated_at": "2024-11-03T22:12:13.916071Z"
}
 */
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
        // const response: Record<string, string> = JSON.parse(event.data);
        // const notification = _.isString(response.notification)
        //   ? JSON.parse(response.notification)
        //   : response.notification;

        // const message: WSMessage = {
        //   type: response.type,
        //   notification,
        // };
        console.log("event.data", event.data);
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

    return () => {
      socket.close();
    };
  }, [client]);

  return { isConnected };
}
