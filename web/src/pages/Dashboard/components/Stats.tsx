import { useSavedCounts } from "@/libs/hooks";
import { CountKey } from "@/libs/types/api";
import { Card, Flex, Heading, Inset, Text } from "@radix-ui/themes";

interface Props {
  scope: CountKey;
}

function titleCase(str: string) {
  return str[0].toUpperCase() + str.slice(1);
}

export function StatCard({ scope }: Props) {
  const context = useSavedCounts();

  return (
    <Card className="w-full">
      <Inset className="border-l-8 border-l-jade-indicator">
        <Flex direction="column" gap="2" className="p-4">
          <Heading className="text-lg font-medium text-slate-9004">
            {titleCase(scope)}
          </Heading>
          {context.isLoading ? <span>Loading</span> : null}
          {context.isError ? <span>Error</span> : null}
          {context.data ? (
            <Text className="text-4xl text-primary font-medium">
              {context.data[scope as CountKey]}
            </Text>
          ) : null}
        </Flex>
      </Inset>
    </Card>
  );
}
