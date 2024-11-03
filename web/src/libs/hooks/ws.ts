/* eslint-disable no-console */
import { useQuery, useQueryClient } from "@tanstack/react-query";
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
  notification: Notification;
};

export function useNotifications() {
  const client = useQueryClient();
  const [messageIDs, setMessageIDs] = useState<string[]>([]);
  useEffect(() => {
    const socket = new WebSocket(
      new URL(
        "/ws/notifications",
        window.location.origin.replace("https", "wss")
      )
    );

    socket.onopen = () => {
      console.debug("Socket opened");
    };

    socket.onmessage = (event: MessageEvent<string>) => {
      try {
        const message: WSMessage = JSON.parse(event.data);

        client.setQueryData(
          ["notifications", message.notification.id],
          message
        );
        console.log(
          "Message",
          message.notification.extras,
          message.notification.task_status
        );

        if (
          message.notification.extras.task_type === "analyze_playlist" &&
          message.notification.extras.playlist_id &&
          message.notification.task_status === "SUCCESS"
        ) {
          client.invalidateQueries({
            queryKey: [
              "browser",
              "playlists",
              message.notification.extras.playlist_id,
            ],
          });
        }

        setMessageIDs((ids) => [...ids, message.notification.id]);
      } catch (error) {
        console.error("Error parsing message", error);
      }
    };

    return () => {
      socket.close();
    };
  }, [client]);
  const query = useQuery({
    queryKey: ["notifications", messageIDs],
    queryFn: async () => {
      return messageIDs;
    },
    enabled: messageIDs.length > 0,
  });

  return { query, client };
}
