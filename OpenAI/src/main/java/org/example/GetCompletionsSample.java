/*
 * © Copyright 2022 by LR Construction Technologies Limited.
 * All rights Reserved.  No part of this document may be reproduced or
 * transmitted in any form or by any means, electronic, mechanical,
 * photocopying, recording, or otherwise, without prior written permission of
 * LR Construction Technologies Limited.
 *
 * @author    patty.hao  (patty.hao@lrctl.com)
 */

package org.example;
//package com.azure.ai.openai.usage;

import com.azure.ai.openai.OpenAIClient;
import com.azure.ai.openai.OpenAIClientBuilder;
import com.azure.ai.openai.models.Choice;
import com.azure.ai.openai.models.Completions;
import com.azure.ai.openai.models.CompletionsOptions;
import com.azure.ai.openai.models.CompletionsUsage;
import com.azure.core.credential.AzureKeyCredential;

import java.util.ArrayList;
import java.util.List;


public class GetCompletionsSample {
    public static void main(String[] args) {
        //String azureOpenaiKey = "9ed7425c56a441658713a0039621f548"; //System.getenv("AZURE_OPENAI_API_KEY");;
        //String endpoint = "https://lr-open-ai-1.openai.azure.com/";//System.getenv("AZURE_OPENAI_ENDPOINT");;
        String azureOpenaiKey = System.getenv("AZURE_OPENAI_API_KEY");;
        String endpoint = System.getenv("AZURE_OPENAI_ENDPOINT");;
        String deploymentOrModelId = "lr-gpt-35-turbo-1";

        OpenAIClient client = new OpenAIClientBuilder()
                .endpoint(endpoint)
                .credential(new AzureKeyCredential(azureOpenaiKey))
                .buildClient();

        List<String> prompt = new ArrayList<>();
        prompt.add("Where was Microsoft founded?");

        Completions completions = client.getCompletions(deploymentOrModelId, new CompletionsOptions(prompt));

        System.out.printf("Model ID=%s is created at %s.%n", completions.getId(), completions.getCreatedAt());
        for (Choice choice : completions.getChoices()) {
            System.out.printf("Index: %d, Text: %s.%n", choice.getIndex(), choice.getText());
        }

        CompletionsUsage usage = completions.getUsage();
        System.out.printf("Usage: number of prompt token is %d, "
                        + "number of completion token is %d, and number of total tokens in request and response is %d.%n",
                usage.getPromptTokens(), usage.getCompletionTokens(), usage.getTotalTokens());
    }
}
