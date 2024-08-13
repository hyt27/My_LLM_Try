plugins {
    java
    application
}
application {
    mainClass.set("GetCompletionsSample")
}
repositories {
    mavenCentral()
}
dependencies {
    implementation(group = "com.azure", name = "azure-ai-openai", version = "1.0.0-beta.3")
    implementation("org.slf4j:slf4j-simple:1.7.9")
}



/*plugins {
    id("java")
    id("application")
}

group = "org.example"
version = "1.0-SNAPSHOT"
application {
    mainClass.set("org.example.GetCompletionsSample")
}

repositories {
    mavenCentral()
}

dependencies {
    implementation(group = "com.azure", name = "azure-ai-openai", version = "1.0.0-beta.3")
    implementation("org.slf4j:slf4j-simple:1.7.9")

    testImplementation(platform("org.junit:junit-bom:5.10.0"))
    testImplementation("org.junit.jupiter:junit-jupiter")
}

tasks.test {
    useJUnitPlatform()
}*/