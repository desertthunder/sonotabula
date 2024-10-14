import { Library } from "./LibraryCard";
import { COUNT_KEYS } from "@/libs/types/api";
import { StatCard } from "./StatCard";
import { Text, Box, Flex } from "@radix-ui/themes";

export default function Dashboard() {
  return (
    <Flex flexGrow="1" gap="8" justify="between" className="px-8 pt-4">
      <Flex direction="column" gap="4">
        <h1 className="text-base font-semibold">Dashboard</h1>
        <Text className="text-sm">
          View your stats and library at a glance.
        </Text>
        <Box flexGrow="1">
          <Library />
        </Box>
      </Flex>

      <Flex direction="column" minWidth="20%" gap="4">
        {COUNT_KEYS.map((key) => (
          <StatCard key={key} scope={key} />
        ))}
      </Flex>
    </Flex>
  );
}
