import { ResourceKey, RESOURCE_KEYS } from "@/libs/types";
import { Tabs as RadixTabs } from "@radix-ui/themes";

interface Props {
  scope: ResourceKey;
  onChange: (key: ResourceKey) => void;
}

const textMap = {
  [ResourceKey.LibraryPlaylists]: "Playlists",
  [ResourceKey.LibraryTracks]: "Tracks",
  [ResourceKey.LibraryAlbums]: "Albums",
  [ResourceKey.LibraryArtists]: "Artists",
} as const;

export function Tabs({ scope, onChange }: Props) {
  return (
    <RadixTabs.Root>
      <RadixTabs.List size="2">
        {RESOURCE_KEYS.map((resource) => {
          return (
            <RadixTabs.Trigger
              key={resource}
              onClick={onChange.bind(null, resource)}
              className={scope === resource ? "active" : ""}
              disabled={scope === resource}
              value={resource}
            >
              {textMap[resource]}
            </RadixTabs.Trigger>
          );
        })}
      </RadixTabs.List>
    </RadixTabs.Root>
  );
}
