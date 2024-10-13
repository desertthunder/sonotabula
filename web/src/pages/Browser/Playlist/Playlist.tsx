import { useCallback, useMemo } from "react";
import { useMatch, useNavigate } from "react-router-dom";
import { Drawer } from "vaul";

export function Playlist() {
  const match = useMatch("/dashboard/browser/playlist/:id");

  const navigate = useNavigate();

  const isOpen = useMemo(() => {
    return !!match;
  }, [match]);

  const onOpenChange = useCallback(
    (open: boolean) => {
      if (!open) {
        navigate("/dashboard/browser");
      }
    },
    [navigate]
  );

  return (
    <Drawer.Root direction="right" open={isOpen} onOpenChange={onOpenChange}>
      <Drawer.Portal>
        <Drawer.Overlay className="fixed inset-0 bg-black/40" />
        <Drawer.Content className="right-0 top-12 bottom-0 fixed z-10 flex outline-none">
          <div className="bg-zinc-50 rounded-md w-1/2 grow mt-2 mr-2 mb-2 p-5 flex flex-col">
            <div className="max-w-md mx-auto">
              <Drawer.Title className="font-medium mb-2 text-zinc-900">
                {match?.params.id}
              </Drawer.Title>
              <Drawer.Description className="text-zinc-600 mb-2">
                Playlist Tracks & Analysis
              </Drawer.Description>
            </div>
          </div>
        </Drawer.Content>
      </Drawer.Portal>
    </Drawer.Root>
  );
}
