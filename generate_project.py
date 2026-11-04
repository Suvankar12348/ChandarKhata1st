import os
import zipfile

# Root project directory
ROOT = "ChandarKhata"

# Define all files and their contents
FILES = {
    # 1. Root build.gradle.kts
    "build.gradle.kts": """
plugins {
    id("com.android.application") version "8.7.2" apply false
    id("org.jetbrains.kotlin.android") version "2.0.21" apply false
    id("org.jetbrains.kotlin.plugin.compose") version "2.0.21" apply false
    id("com.google.devtools.ksp") version "2.0.21-1.0.27" apply false
}
""",

    # 2. settings.gradle.kts
    "settings.gradle.kts": """
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "ChandarKhata"
include(":app")
""",

    # 3. gradle.properties
    "gradle.properties": """
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
""",

    # 4. app/build.gradle.kts
    "app/build.gradle.kts": """
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("com.google.devtools.ksp")
    id("org.jetbrains.kotlin.plugin.compose")
    id("kotlin-parcelize")
}

android {
    namespace = "com.chandarkhata.app"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.chandarkhata.app"
        minSdk = 24
        targetSdk = 35
        versionCode = 1
        versionName = "1.0.0-offline"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
    buildFeatures {
        compose = true
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.15.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.7")
    implementation("androidx.activity:activity-compose:1.9.3")

    implementation(platform("androidx.compose:compose-bom:2024.11.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3:1.3.1")
    implementation("androidx.compose.material:material-icons-extended:1.7.5")
    implementation("androidx.navigation:navigation-compose:2.8.4")

    val roomVersion = "2.6.1"
    implementation("androidx.room:room-runtime:$roomVersion")
    implementation("androidx.room:room-ktx:$roomVersion")
    ksp("androidx.room:room-compiler:$roomVersion")

    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.7")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.8.7")
    implementation("com.google.code.gson:gson:2.11.0")
}
""",

    # 5. AndroidManifest.xml
    "app/src/main/AndroidManifest.xml": """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:name=".ChandarKhataApp"
        android:allowBackup="true"
        android:label="চাঁদার খাতা"
        android:supportsRtl="true"
        android:theme="@android:style/Theme.Material.Light.NoActionBar">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:windowSoftInputMode="adjustResize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        <provider
            android:name="androidx.core.content.FileProvider"
            android:authorities="com.chandarkhata.app.fileprovider"
            android:exported="false"
            android:grantUriPermissions="true">
            <meta-data
                android:name="android.support.FILE_PROVIDER_PATHS"
                android:resource="@xml/file_paths" />
        </provider>
    </application>
</manifest>
""",

    # 6. file_paths.xml
    "app/src/main/res/xml/file_paths.xml": """<?xml version="1.0" encoding="utf-8"?>
<paths>
    <cache-path name="receipts" path="receipts/" />
    <cache-path name="backups" path="backups/" />
    <files-path name="internal_files" path="." />
</paths>
""",

    # 7. GitHub Actions Cloud Builder Workflow
    ".github/workflows/build.yml": """name: Build Chandar Khata APK

on:
  push:
    branches: [ "main", "master" ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Source Code
        uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v3

      - name: Generate Gradle Wrapper
        run: gradle wrapper

      - name: Build Debug APK
        run: ./gradlew assembleDebug --stacktrace

      - name: Upload Debug APK
        uses: actions/upload-artifact@v4
        with:
          name: ChandarKhata-Debug-APK
          path: app/build/outputs/apk/debug/app-debug.apk
""",

    # 8. ChandarKhataApp.kt
    "app/src/main/java/com/chandarkhata/app/ChandarKhataApp.kt": """package com.chandarkhata.app

import android.app.Application
import com.chandarkhata.app.data.database.AppDatabase
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.SupervisorJob

class ChandarKhataApp : Application() {
    val applicationScope = CoroutineScope(SupervisorJob())
    val database by lazy { AppDatabase.getDatabase(this, applicationScope) }
}
""",

    # 9. Entities.kt
    "app/src/main/java/com/chandarkhata/app/data/model/Entities.kt": """package com.chandarkhata.app.data.model

import androidx.room.*

@Entity(tableName = "committees")
data class Committee(
    @PrimaryKey val id: Long = 1L,
    val name: String = "Sarbojanin Puja Committee",
    val bengaliName: String = "সর্বজনীন পূজা সমিতি",
    val address: String = "Kolkata, West Bengal",
    val contactNumber: String = "9876543210"
)

@Entity(tableName = "events")
data class Event(
    @PrimaryKey(autoGenerate = true) val id: Long = 0L,
    val name: String,
    val year: Int,
    val budget: Double = 0.0,
    val isCurrent: Boolean = false
)

enum class DonorCategory { HOUSEHOLD, SHOP_BUSINESS, ORGANISATION }

@Entity(tableName = "donors")
data class Donor(
    @PrimaryKey(autoGenerate = true) val id: Long = 0L,
    val fullName: String,
    val address: String,
    val contactNumber: String,
    val whatsappNumber: String,
    val category: DonorCategory = DonorCategory.HOUSEHOLD,
    val isDemo: Boolean = false
)

enum class PaymentStatus { UNPAID, PARTIALLY_PAID, PAID }

@Entity(
    tableName = "bills",
    foreignKeys = [
        ForeignKey(entity = Donor::class, parentColumns = ["id"], childColumns = ["donorId"], onDelete = ForeignKey.CASCADE),
        ForeignKey(entity = Event::class, parentColumns = ["id"], childColumns = ["eventId"], onDelete = ForeignKey.RESTRICT)
    ],
    indices = [Index("donorId"), Index("eventId"), Index(value = ["billNumber"], unique = true)]
)
data class DonationBill(
    @PrimaryKey(autoGenerate = true) val id: Long = 0L,
    val billNumber: String,
    val donorId: Long,
    val eventId: Long,
    val billAmount: Double,
    val totalReceived: Double = 0.0,
    val balanceDue: Double = billAmount,
    val paymentStatus: PaymentStatus = PaymentStatus.UNPAID,
    val billDate: Long = System.currentTimeMillis(),
    val isDemo: Boolean = false
)

enum class PaymentMethod { CASH, UPI, MIXED }

@Entity(
    tableName = "payments",
    foreignKeys = [
        ForeignKey(entity = DonationBill::class, parentColumns = ["id"], childColumns = ["billId"], onDelete = ForeignKey.CASCADE)
    ],
    indices = [Index("billId")]
)
data class DonationPayment(
    @PrimaryKey(autoGenerate = true) val id: Long = 0L,
    val billId: Long,
    val amount: Double,
    val paymentMethod: PaymentMethod,
    val cashAmount: Double = 0.0,
    val upiAmount: Double = 0.0,
    val paymentDate: Long = System.currentTimeMillis(),
    val collectorName: String,
    val transactionRef: String = "",
    val isDemo: Boolean = false
)

@Entity(tableName = "volunteers")
data class Volunteer(
    @PrimaryKey(autoGenerate = true) val id: Long = 0L,
    val name: String,
    val phone: String,
    val role: String = "Collector"
)

enum class ExpenseCategory { IDOL_MURTI, PANDAL, LIGHTING, PUJA_SAMAGRI, BHOG_PRASAD, MISC }

@Entity(
    tableName = "expenses",
    foreignKeys = [
        ForeignKey(entity = Event::class, parentColumns = ["id"], childColumns = ["eventId"], onDelete = ForeignKey.RESTRICT)
    ],
    indices = [Index("eventId")]
)
data class Expense(
    @PrimaryKey(autoGenerate = true) val id: Long = 0L,
    val eventId: Long,
    val category: ExpenseCategory,
    val amount: Double,
    val description: String,
    val paymentMethod: PaymentMethod = PaymentMethod.CASH,
    val expenseDate: Long = System.currentTimeMillis(),
    val isDemo: Boolean = false
)
""",

    # 10. ChandarKhataDao.kt
    "app/src/main/java/com/chandarkhata/app/data/dao/ChandarKhataDao.kt": """package com.chandarkhata.app.data.dao

import androidx.room.*
import com.chandarkhata.app.data.model.*
import kotlinx.coroutines.flow.Flow

data class BillWithDonor(
    @Embedded val bill: DonationBill,
    @Relation(parentColumn = "donorId", entityColumn = "id")
    val donor: Donor,
    @Relation(parentColumn = "eventId", entityColumn = "id")
    val event: Event
)

data class BillWithDonorAndPayments(
    @Embedded val bill: DonationBill,
    @Relation(parentColumn = "donorId", entityColumn = "id")
    val donor: Donor,
    @Relation(parentColumn = "eventId", entityColumn = "id")
    val event: Event,
    @Relation(parentColumn = "id", entityColumn = "billId")
    val payments: List<DonationPayment>
)

data class DonorWithBills(
    @Embedded val donor: Donor,
    @Relation(entity = DonationBill::class, parentColumn = "id", entityColumn = "donorId")
    val billsWithPayments: List<BillWithPayments>
)

data class BillWithPayments(
    @Embedded val bill: DonationBill,
    @Relation(parentColumn = "id", entityColumn = "billId")
    val payments: List<DonationPayment>,
    @Relation(parentColumn = "eventId", entityColumn = "id")
    val event: Event
)

@Dao
interface ChandarKhataDao {
    @Query("SELECT * FROM committees WHERE id = 1 LIMIT 1")
    fun getCommittee(): Flow<Committee?>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun saveCommittee(committee: Committee)

    @Query("SELECT * FROM events ORDER BY year DESC, id DESC")
    fun getAllEvents(): Flow<List<Event>>

    @Query("SELECT * FROM events WHERE isCurrent = 1 LIMIT 1")
    fun getCurrentEvent(): Flow<Event?>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertEvent(event: Event): Long

    @Query("UPDATE events SET isCurrent = CASE WHEN id = :selectedEventId THEN 1 ELSE 0 END")
    suspend fun setCurrentEvent(selectedEventId: Long)

    @Insert(onConflict = OnConflictStrategy.ABORT)
    suspend fun insertDonor(donor: Donor): Long

    @Query("SELECT * FROM donors WHERE contactNumber = :phone OR whatsappNumber = :phone LIMIT 1")
    suspend fun findDonorByPhone(phone: String): Donor?

    @Query("SELECT * FROM donors ORDER BY fullName ASC")
    fun getAllDonors(): Flow<List<Donor>>

    @Transaction
    @Query("SELECT * FROM donors WHERE id = :donorId")
    fun getDonorProfile(donorId: Long): Flow<DonorWithBills>

    @Insert
    suspend fun insertBill(bill: DonationBill): Long

    @Update
    suspend fun updateBill(bill: DonationBill)

    @Transaction
    @Query("SELECT * FROM bills WHERE eventId = :eventId ORDER BY id DESC")
    fun getBillsForEvent(eventId: Long): Flow<List<BillWithDonor>>

    @Transaction
    @Query("SELECT * FROM bills WHERE eventId = :eventId AND paymentStatus != 'PAID' ORDER BY balanceDue DESC")
    fun getPendingBillsForEvent(eventId: Long): Flow<List<BillWithDonor>>

    @Transaction
    @Query("SELECT * FROM bills WHERE id = :billId")
    fun getBillDetail(billId: Long): Flow<BillWithDonorAndPayments?>

    @Query("SELECT COUNT(*) FROM bills WHERE eventId = :eventId")
    suspend fun getBillCountForEvent(eventId: Long): Int

    @Insert
    suspend fun insertPayment(payment: DonationPayment): Long

    @Query("SELECT * FROM payments ORDER BY paymentDate DESC")
    fun getAllPayments(): Flow<List<DonationPayment>>

    @Transaction
    suspend fun recordPaymentAndUpdateBill(payment: DonationPayment) {
        insertPayment(payment)
        val bill = getRawBill(payment.billId) ?: return
        val newReceived = bill.totalReceived + payment.amount
        val newDue = (bill.billAmount - newReceived).coerceAtLeast(0.0)
        val newStatus = when {
            newDue <= 0.0 -> PaymentStatus.PAID
            newReceived > 0.0 -> PaymentStatus.PARTIALLY_PAID
            else -> PaymentStatus.UNPAID
        }
        updateBill(bill.copy(totalReceived = newReceived, balanceDue = newDue, paymentStatus = newStatus))
    }

    @Query("SELECT * FROM bills WHERE id = :billId LIMIT 1")
    suspend fun getRawBill(billId: Long): DonationBill?

    @Query("SELECT * FROM volunteers ORDER BY name ASC")
    fun getAllVolunteers(): Flow<List<Volunteer>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertVolunteer(volunteer: Volunteer): Long

    @Query("SELECT * FROM expenses WHERE eventId = :eventId ORDER BY expenseDate DESC")
    fun getExpensesForEvent(eventId: Long): Flow<List<Expense>>

    @Insert
    suspend fun insertExpense(expense: Expense): Long

    @Query("DELETE FROM payments WHERE isDemo = 1")
    suspend fun clearDemoPayments()

    @Query("DELETE FROM bills WHERE isDemo = 1")
    suspend fun clearDemoBills()

    @Query("DELETE FROM donors WHERE isDemo = 1")
    suspend fun clearDemoDonors()

    @Query("DELETE FROM expenses WHERE isDemo = 1")
    suspend fun clearDemoExpenses()
}
""",

    # 11. AppDatabase.kt
    "app/src/main/java/com/chandarkhata/app/data/database/AppDatabase.kt": """package com.chandarkhata.app.data.database

import android.content.Context
import androidx.room.*
import androidx.sqlite.db.SupportSQLiteDatabase
import com.chandarkhata.app.data.dao.ChandarKhataDao
import com.chandarkhata.app.data.model.*
import kotlinx.coroutines.*

@Database(
    entities = [Committee::class, Event::class, Donor::class, DonationBill::class, DonationPayment::class, Volunteer::class, Expense::class],
    version = 1,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun chandarKhataDao(): ChandarKhataDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getDatabase(context: Context, scope: CoroutineScope): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "chandar_khata_database.db"
                )
                .addCallback(object : RoomDatabase.Callback() {
                    override fun onCreate(db: SupportSQLiteDatabase) {
                        super.onCreate(db)
                        INSTANCE?.let { database ->
                            scope.launch(Dispatchers.IO) {
                                val dao = database.chandarKhataDao()
                                dao.saveCommittee(
                                    Committee(1L, "Ekota Sangha Sarbojanin Durgotsab", "একতা সংঘ সর্বজনীন দুর্গোৎসব", "Kolkata, WB", "9830012345")
                                )
                                val eventId = dao.insertEvent(Event(name = "Durga Puja", year = 2026, budget = 500000.0, isCurrent = true))
                                dao.setCurrentEvent(eventId)
                                dao.insertVolunteer(Volunteer(name = "Subhasish Roy", phone = "9831100001", role = "Lead Collector"))
                                dao.insertVolunteer(Volunteer(name = "Anirban Sen", phone = "9831100002", role = "Treasurer"))
                            }
                        }
                    }
                })
                .build()
                INSTANCE = instance
                instance
            }
        }
    }
}
""",

    # 12. Colors & Theme
    "app/src/main/java/com/chandarkhata/app/ui/theme/Color.kt": """package com.chandarkhata.app.ui.theme

import androidx.compose.ui.graphics.Color

val PurplePrimary = Color(0xFF4A148C)
val PurpleDark = Color(0xFF311B92)
val PurpleLight = Color(0xFF7C43BD)
val LavenderCard = Color(0xFFF3E5F5)
val SurfacePale = Color(0xFFF8F9FA)
val AccentYellow = Color(0xFFFFD600)
val StatusGreenPaid = Color(0xFF2E7D32)
val StatusGreenBg = Color(0xFFE8F5E9)
val StatusRedDue = Color(0xFFC62828)
val StatusRedBg = Color(0xFFFFEBEE)
val TextDark = Color(0xFF212121)
val TextMuted = Color(0xFF757575)
""",

    "app/src/main/java/com/chandarkhata/app/ui/theme/Theme.kt": """package com.chandarkhata.app.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val LightColorScheme = lightColorScheme(
    primary = PurplePrimary,
    onPrimary = Color.White,
    primaryContainer = LavenderCard,
    onPrimaryContainer = PurpleDark,
    secondary = PurpleLight,
    onSecondary = Color.White,
    background = Color(0xFFFBFBFC),
    surface = Color.White,
    onSurface = TextDark,
    surfaceVariant = SurfacePale
)

@Composable
fun ChandarKhataTheme(content: @Composable () -> Unit) {
    MaterialTheme(colorScheme = LightColorScheme, content = content)
}
""",

    # 13. Screen Navigation
    "app/src/main/java/com/chandarkhata/app/ui/navigation/Screen.kt": """package com.chandarkhata.app.ui.navigation

sealed class Screen(val route: String, val titleBengali: String, val titleEnglish: String) {
    object Dashboard : Screen("dashboard", "ড্যাশবোর্ড", "Dashboard")
    object NewEntry : Screen("new_entry", "নতুন চাঁদা", "New Entry")
    object PendingDues : Screen("pending_dues", "বকেয়া", "Pending Dues")
    object Donors : Screen("donors", "দাতা", "Donors")
    object Settings : Screen("settings", "সেটিংস", "Settings")
    object BillDetail : Screen("bill_detail/{billId}", "রসিদ বিবরণ", "Bill Detail") {
        fun createRoute(billId: Long) = "bill_detail/$billId"
    }
}
""",

    # 14. ViewModel
    "app/src/main/java/com/chandarkhata/app/ui/viewmodel/KhataViewModel.kt": """package com.chandarkhata.app.ui.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.chandarkhata.app.ChandarKhataApp
import com.chandarkhata.app.data.dao.*
import com.chandarkhata.app.data.model.*
import com.chandarkhata.app.util.DemoDataGenerator
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

data class DashboardSummary(
    val totalBillsCount: Int = 0,
    val totalBilledAmount: Double = 0.0,
    val totalReceivedAmount: Double = 0.0,
    val outstandingAmount: Double = 0.0,
    val todayCollection: Double = 0.0,
    val cashCollection: Double = 0.0,
    val upiCollection: Double = 0.0,
    val pendingBillsCount: Int = 0
)

class KhataViewModel(application: Application) : AndroidViewModel(application) {
    private val dao = (application as ChandarKhataApp).database.chandarKhataDao()

    val committee = dao.getCommittee().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), null)
    val allEvents = dao.getAllEvents().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
    val currentEvent = dao.getCurrentEvent().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), null)

    val currentBills: StateFlow<List<BillWithDonor>> = currentEvent
        .filterNotNull()
        .flatMapLatest { dao.getBillsForEvent(it.id) }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    val pendingBills: StateFlow<List<BillWithDonor>> = currentEvent
        .filterNotNull()
        .flatMapLatest { dao.getPendingBillsForEvent(it.id) }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    val allDonors = dao.getAllDonors().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
    val volunteers = dao.getAllVolunteers().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    val dashboardSummary: StateFlow<DashboardSummary> = combine(currentBills, dao.getAllPayments()) { bills, payments ->
        val billed = bills.sumOf { it.bill.billAmount }
        val received = bills.sumOf { it.bill.totalReceived }
        val due = bills.sumOf { it.bill.balanceDue }
        val pendingCount = bills.count { it.bill.paymentStatus != PaymentStatus.PAID }
        val todayStart = System.currentTimeMillis() - (System.currentTimeMillis() % (24 * 60 * 60 * 1000))
        val today = payments.filter { it.paymentDate >= todayStart }.sumOf { it.amount }
        val cash = payments.sumOf { it.cashAmount }
        val upi = payments.sumOf { it.upiAmount }
        DashboardSummary(bills.size, billed, received, due, today, cash, upi, pendingCount)
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), DashboardSummary())

    fun selectEvent(eventId: Long) = viewModelScope.launch(Dispatchers.IO) { dao.setCurrentEvent(eventId) }

    fun addNewEvent(name: String, year: Int, budget: Double) = viewModelScope.launch(Dispatchers.IO) {
        val id = dao.insertEvent(Event(name = name, year = year, budget = budget, isCurrent = true))
        dao.setCurrentEvent(id)
    }

    suspend fun saveAndCreateBill(name: String, address: String, contact: String, amount: Double): Long {
        val event = currentEvent.value ?: return -1L
        val existing = dao.findDonorByPhone(contact.trim())
        val donorId = existing?.id ?: dao.insertDonor(
            Donor(fullName = name.trim(), address = address.trim(), contactNumber = contact.trim(), whatsappNumber = contact.trim())
        )
        val count = dao.getBillCountForEvent(event.id) + 1
        val billNumber = "CK-${event.year}-${count.toString().padStart(4, '0')}"
        return dao.insertBill(
            DonationBill(billNumber = billNumber, donorId = donorId, eventId = event.id, billAmount = amount)
        )
    }

    fun getBillDetail(billId: Long) = dao.getBillDetail(billId)

    fun recordPayment(billId: Long, amount: Double, method: PaymentMethod, cashPart: Double, upiPart: Double, collector: String) {
        viewModelScope.launch(Dispatchers.IO) {
            dao.recordPaymentAndUpdateBill(
                DonationPayment(billId = billId, amount = amount, paymentMethod = method, cashAmount = cashPart, upiAmount = upiPart, collectorName = collector)
            )
        }
    }

    fun loadDemoData() = viewModelScope.launch(Dispatchers.IO) { DemoDataGenerator.populateDemoData(dao) }

    fun clearDemoData() = viewModelScope.launch(Dispatchers.IO) {
        dao.clearDemoPayments()
        dao.clearDemoBills()
        dao.clearDemoDonors()
        dao.clearDemoExpenses()
    }
}
""",

    # 15. DashboardScreen.kt
    "app/src/main/java/com/chandarkhata/app/ui/screens/DashboardScreen.kt": """package com.chandarkhata.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.chandarkhata.app.ui.theme.*
import com.chandarkhata.app.ui.viewmodel.KhataViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DashboardScreen(
    viewModel: KhataViewModel,
    onNavigateToNewEntry: () -> Unit,
    onNavigateToPendingDues: () -> Unit,
    onBillClick: (Long) -> Unit
) {
    val summary by viewModel.dashboardSummary.collectAsState()
    val currentEvent by viewModel.currentEvent.collectAsState()
    val recentBills by viewModel.currentBills.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text("চাঁদার খাতা • Chandar Khata", fontWeight = FontWeight.Bold, fontSize = 18.sp)
                        Text("${currentEvent?.name ?: "Puja"} ${currentEvent?.year ?: 2026}", style = MaterialTheme.typography.bodySmall, color = AccentYellow)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = PurplePrimary, titleContentColor = Color.White)
            )
        },
        floatingActionButton = {
            ExtendedFloatingActionButton(
                onClick = onNavigateToNewEntry,
                containerColor = PurplePrimary,
                contentColor = Color.White,
                icon = { Icon(Icons.Default.Add, null) },
                text = { Text("নতুন চাঁদা / New Entry", fontWeight = FontWeight.Bold) }
            )
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(padding).background(MaterialTheme.colorScheme.background).padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            item {
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = PurpleDark)
                ) {
                    Column(modifier = Modifier.padding(18.dp)) {
                        Text("মোট সংগৃহীত চাঁদা (Total Received)", color = Color.White.copy(alpha = 0.8f), fontSize = 13.sp)
                        Text("₹${String.format("%,.0f", summary.totalReceivedAmount)}", color = AccentYellow, fontSize = 32.sp, fontWeight = FontWeight.ExtraBold)
                        Spacer(Modifier.height(10.dp))
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            Column {
                                Text("আজকের আদায় (Today)", color = Color.White.copy(alpha = 0.7f), fontSize = 11.sp)
                                Text("₹${summary.todayCollection.toInt()}", color = Color.White, fontWeight = FontWeight.SemiBold)
                            }
                            Column {
                                Text("নগদ (Cash)", color = Color.White.copy(alpha = 0.7f), fontSize = 11.sp)
                                Text("₹${summary.cashCollection.toInt()}", color = Color.White, fontWeight = FontWeight.SemiBold)
                            }
                            Column {
                                Text("অনলাইন (UPI)", color = Color.White.copy(alpha = 0.7f), fontSize = 11.sp)
                                Text("₹${summary.upiCollection.toInt()}", color = Color.White, fontWeight = FontWeight.SemiBold)
                            }
                        }
                    }
                }
            }
            item {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    Card(modifier = Modifier.weight(1f), colors = CardDefaults.cardColors(containerColor = LavenderCard)) {
                        Column(modifier = Modifier.padding(14.dp)) {
                            Text("মোট নির্ধারিত", fontSize = 12.sp, color = PurpleDark)
                            Text("₹${summary.totalBilledAmount.toInt()}", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = PurplePrimary)
                            Text("${summary.totalBillsCount} টি রসিদ", fontSize = 11.sp, color = TextMuted)
                        }
                    }
                    Card(
                        modifier = Modifier.weight(1f).clickable { onNavigateToPendingDues() },
                        colors = CardDefaults.cardColors(containerColor = StatusRedBg)
                    ) {
                        Column(modifier = Modifier.padding(14.dp)) {
                            Text("মোট বকেয়া (Dues)", fontSize = 12.sp, color = StatusRedDue)
                            Text("₹${summary.outstandingAmount.toInt()}", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = StatusRedDue)
                            Text("${summary.pendingBillsCount} জনের বাকি ›", fontSize = 11.sp, color = StatusRedDue, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }
            item {
                Text("সাম্প্রতিক চাঁদা এন্ট্রি (Recent Bills)", fontSize = 15.sp, fontWeight = FontWeight.Bold)
            }
            items(recentBills.take(5).size) { index ->
                val item = recentBills[index]
                Card(
                    modifier = Modifier.fillMaxWidth().clickable { onBillClick(item.bill.id) },
                    colors = CardDefaults.cardColors(containerColor = Color.White)
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth().padding(14.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text(item.donor.fullName, fontWeight = FontWeight.Bold)
                            Text(item.bill.billNumber, fontSize = 11.sp, color = TextMuted)
                        }
                        Column(horizontalAlignment = Alignment.End) {
                            Text("₹${item.bill.billAmount.toInt()}", fontWeight = FontWeight.Bold, color = PurplePrimary)
                            Text(
                                if (item.bill.balanceDue <= 0) "PAID" else "DUE: ₹${item.bill.balanceDue.toInt()}",
                                color = if (item.bill.balanceDue <= 0) StatusGreenPaid else StatusRedDue,
                                fontWeight = FontWeight.Bold,
                                fontSize = 11.sp
                            )
                        }
                    }
                }
            }
        }
    }
}
""",

    # 16. NewEntryScreen.kt (Strict 4 Fields)
    "app/src/main/java/com/chandarkhata/app/ui/screens/NewEntryScreen.kt": """package com.chandarkhata.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.chandarkhata.app.ui.theme.*
import com.chandarkhata.app.ui.viewmodel.KhataViewModel
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NewEntryScreen(
    viewModel: KhataViewModel,
    onBillCreated: (Long) -> Unit,
    onBack: () -> Unit
) {
    val coroutineScope = rememberCoroutineScope()
    var name by remember { mutableStateOf("") }
    var address by remember { mutableStateOf("") }
    var contactNumber by remember { mutableStateOf("") }
    var donationAmount by remember { mutableStateOf("") }
    var isSaving by remember { mutableStateOf(false) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("নতুন চাঁদা এন্ট্রি • New Entry", fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onBack) { Icon(Icons.Default.ArrowBack, null, tint = Color.White) }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = PurplePrimary, titleContentColor = Color.White)
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier.fillMaxSize().padding(padding).background(MaterialTheme.colorScheme.background).padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            OutlinedTextField(
                value = name,
                onValueChange = { name = it },
                label = { Text("১. দাতার নাম (Donor Name) *") },
                leadingIcon = { Icon(Icons.Default.Person, null) },
                modifier = Modifier.fillMaxWidth()
            )
            OutlinedTextField(
                value = address,
                onValueChange = { address = it },
                label = { Text("২. ঠিকানা (Address) *") },
                leadingIcon = { Icon(Icons.Default.Home, null) },
                modifier = Modifier.fillMaxWidth()
            )
            OutlinedTextField(
                value = contactNumber,
                onValueChange = { contactNumber = it },
                label = { Text("৩. ফোন / হোয়াটসঅ্যাপ নম্বর *") },
                leadingIcon = { Icon(Icons.Default.Phone, null) },
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Phone),
                modifier = Modifier.fillMaxWidth()
            )
            OutlinedTextField(
                value = donationAmount,
                onValueChange = { donationAmount = it },
                label = { Text("৪. চাঁদার পরিমাণ (Donation Amount ₹) *") },
                leadingIcon = { Icon(Icons.Default.CurrencyRupee, null) },
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(Modifier.height(10.dp))

            Button(
                onClick = {
                    val amt = donationAmount.toDoubleOrNull()
                    if (name.isNotBlank() && address.isNotBlank() && contactNumber.length >= 10 && amt != null && amt > 0) {
                        isSaving = true
                        coroutineScope.launch {
                            val id = viewModel.saveAndCreateBill(name, address, contactNumber, amt)
                            if (id > 0) onBillCreated(id)
                            isSaving = false
                        }
                    }
                },
                modifier = Modifier.fillMaxWidth().height(52.dp),
                colors = ButtonDefaults.buttonColors(containerColor = PurplePrimary),
                enabled = !isSaving
            ) {
                if (isSaving) CircularProgressIndicator(color = Color.White, modifier = Modifier.size(24.dp))
                else Text("SAVE & CREATE BILL", fontSize = 16.sp, fontWeight = FontWeight.Bold)
            }
        }
    }
}
""",

    # 17. BillDetailScreen.kt
    "app/src/main/java/com/chandarkhata/app/ui/screens/BillDetailScreen.kt": """package com.chandarkhata.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.chandarkhata.app.data.model.PaymentMethod
import com.chandarkhata.app.data.model.PaymentStatus
import com.chandarkhata.app.ui.theme.*
import com.chandarkhata.app.ui.viewmodel.KhataViewModel
import com.chandarkhata.app.util.PdfReceiptGenerator

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BillDetailScreen(
    billId: Long,
    viewModel: KhataViewModel,
    onBack: () -> Unit
) {
    val context = LocalContext.current
    val billDetail by viewModel.getBillDetail(billId).collectAsState(initial = null)
    val committee by viewModel.committee.collectAsState()
    var showPaymentDialog by remember { mutableStateOf(false) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(billDetail?.bill?.billNumber ?: "রসিদ বিবরণী", fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onBack) { Icon(Icons.Default.ArrowBack, null, tint = Color.White) }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = PurplePrimary, titleContentColor = Color.White),
                actions = {
                    if (billDetail != null && committee != null) {
                        IconButton(onClick = { PdfReceiptGenerator.generateAndSharePdf(context, billDetail!!, committee!!) }) {
                            Icon(Icons.Default.Share, "Share Receipt", tint = Color.White)
                        }
                    }
                }
            )
        },
        bottomBar = {
            if (billDetail != null && billDetail!!.bill.balanceDue > 0) {
                Surface(shadowElevation = 8.dp) {
                    Box(modifier = Modifier.padding(16.dp)) {
                        Button(
                            onClick = { showPaymentDialog = true },
                            modifier = Modifier.fillMaxWidth().height(48.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = StatusGreenPaid)
                        ) {
                            Text("টাকা জমা নিন / COLLECT PAYMENT", fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }
        }
    ) { padding ->
        billDetail?.let { detail ->
            LazyColumn(
                modifier = Modifier.fillMaxSize().padding(padding).background(MaterialTheme.colorScheme.background).padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(14.dp)
            ) {
                item {
                    Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = LavenderCard)) {
                        Row(modifier = Modifier.padding(16.dp).fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            Column {
                                Text("স্ট্যাটাস (Status)", fontSize = 12.sp, color = TextMuted)
                                Text(detail.bill.paymentStatus.name, fontSize = 18.sp, fontWeight = FontWeight.ExtraBold, color = PurplePrimary)
                            }
                            Column(horizontalAlignment = Alignment.End) {
                                Text("বাকি (Due)", fontSize = 12.sp, color = TextMuted)
                                Text("₹${detail.bill.balanceDue.toInt()}", fontSize = 20.sp, fontWeight = FontWeight.ExtraBold, color = StatusRedDue)
                            }
                        }
                    }
                }
                item {
                    Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = Color.White)) {
                        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                            Text("দাতার নাম: ${detail.donor.fullName}", fontWeight = FontWeight.SemiBold)
                            Text("ঠিকানা: ${detail.donor.address}", fontSize = 13.sp)
                            Text("ফোন: ${detail.donor.contactNumber}", fontSize = 13.sp)
                            Text("ধার্য চাঁদা: ₹${detail.bill.billAmount.toInt()}", fontWeight = FontWeight.Bold, color = PurplePrimary)
                        }
                    }
                }
                item { Text("জমা বিবরণী (Payment History)", fontWeight = FontWeight.Bold) }
                items(detail.payments) { pay ->
                    Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = Color.White)) {
                        Row(modifier = Modifier.padding(14.dp).fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            Column {
                                Text("জমা: ₹${pay.amount.toInt()}", fontWeight = FontWeight.Bold, color = StatusGreenPaid)
                                Text("মাধ্যম: ${pay.paymentMethod.name}", fontSize = 12.sp, color = TextMuted)
                            }
                            Text(pay.collectorName, fontSize = 12.sp, color = TextMuted)
                        }
                    }
                }
            }

            if (showPaymentDialog) {
                var amtInput by remember { mutableStateOf(detail.bill.balanceDue.toInt().toString()) }
                AlertDialog(
                    onDismissRequest = { showPaymentDialog = false },
                    title = { Text("টাকা গ্রহণ / Collect Payment") },
                    text = {
                        OutlinedTextField(
                            value = amtInput,
                            onValueChange = { amtInput = it },
                            label = { Text("টাকার অঙ্ক (₹)") },
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                            modifier = Modifier.fillMaxWidth()
                        )
                    },
                    confirmButton = {
                        Button(onClick = {
                            val a = amtInput.toDoubleOrNull()
                            if (a != null && a > 0 && a <= detail.bill.balanceDue) {
                                viewModel.recordPayment(detail.bill.id, a, PaymentMethod.CASH, a, 0.0, "Volunteer")
                                showPaymentDialog = false
                            }
                        }) { Text("Confirm") }
                    },
                    dismissButton = { TextButton(onClick = { showPaymentDialog = false }) { Text("Cancel") } }
                )
            }
        } ?: Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { CircularProgressIndicator() }
    }
}
""",

    # 18. PendingDuesScreen.kt
    "app/src/main/java/com/chandarkhata/app/ui/screens/PendingDuesScreen.kt": """package com.chandarkhata.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.chandarkhata.app.ui.theme.*
import com.chandarkhata.app.ui.viewmodel.KhataViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PendingDuesScreen(
    viewModel: KhataViewModel,
    onOpenBill: (Long) -> Unit,
    onBack: () -> Unit
) {
    val pendingBills by viewModel.pendingBills.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("বকেয়া তালিকা • Pending Dues", fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onBack) { Icon(Icons.Default.ArrowBack, null, tint = Color.White) }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = PurplePrimary, titleContentColor = Color.White)
            )
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(padding).background(MaterialTheme.colorScheme.background).padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            items(pendingBills) { item ->
                Card(
                    modifier = Modifier.fillMaxWidth().clickable { onOpenBill(item.bill.id) },
                    colors = CardDefaults.cardColors(containerColor = Color.White)
                ) {
                    Column(modifier = Modifier.padding(14.dp)) {
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text(item.donor.fullName, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                                Text("রসিদ নং: ${item.bill.billNumber}", fontSize = 11.sp, color = TextMuted)
                            }
                            Column(horizontalAlignment = Alignment.End) {
                                Text("বাকি ₹${item.bill.balanceDue.toInt()}", fontWeight = FontWeight.Bold, color = StatusRedDue)
                                Text("মোট ₹${item.bill.billAmount.toInt()}", fontSize = 11.sp, color = TextMuted)
                            }
                        }
                        Spacer(Modifier.height(8.dp))
                        Button(
                            onClick = { onOpenBill(item.bill.id) },
                            modifier = Modifier.fillMaxWidth(),
                            colors = ButtonDefaults.buttonColors(containerColor = PurplePrimary)
                        ) {
                            Text("COLLECT DUE")
                        }
                    }
                }
            }
        }
    }
}
""",

    # 19. DonorsScreen.kt
    "app/src/main/java/com/chandarkhata/app/ui/screens/DonorsScreen.kt": """package com.chandarkhata.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.chandarkhata.app.ui.theme.*
import com.chandarkhata.app.ui.viewmodel.KhataViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DonorsScreen(viewModel: KhataViewModel) {
    val donors by viewModel.allDonors.collectAsState()
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("দাতা তালিকা • Donors", fontWeight = FontWeight.Bold) },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = PurplePrimary, titleContentColor = Color.White)
            )
        }
    ) { padding ->
        LazyColumn(modifier = Modifier.fillMaxSize().padding(padding).padding(14.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            items(donors) { donor ->
                Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = Color.White)) {
                    Column(modifier = Modifier.padding(14.dp)) {
                        Text(donor.fullName, fontWeight = FontWeight.Bold, fontSize = 15.sp)
                        Text(donor.address, fontSize = 12.sp, color = TextMuted)
                        Text("📞 ${donor.contactNumber}", fontSize = 11.sp, color = TextMuted)
                    }
                }
            }
        }
    }
}
""",

    # 20. SettingsScreen.kt
    "app/src/main/java/com/chandarkhata/app/ui/screens/SettingsScreen.kt": """package com.chandarkhata.app.ui.screens

import android.widget.Toast
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.chandarkhata.app.ui.theme.PurplePrimary
import com.chandarkhata.app.ui.theme.StatusRedDue
import com.chandarkhata.app.ui.viewmodel.KhataViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(viewModel: KhataViewModel) {
    val context = LocalContext.current
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("সেটিংস • Settings", fontWeight = FontWeight.Bold) },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = PurplePrimary, titleContentColor = Color.White)
            )
        }
    ) { padding ->
        Column(modifier = Modifier.fillMaxSize().padding(padding).padding(16.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
            Card(modifier = Modifier.fillMaxWidth()) {
                Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text("নমুনা ডেমো ডেটা (Demo Data)", fontWeight = FontWeight.Bold)
                    Button(
                        onClick = {
                            viewModel.loadDemoData()
                            Toast.makeText(context, "নমুনা ডেটা যোগ হয়েছে", Toast.LENGTH_SHORT).show()
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text("Generate Demo Data")
                    }
                    OutlinedButton(
                        onClick = {
                            viewModel.clearDemoData()
                            Toast.makeText(context, "ডেমো ডেটা মুছে ফেলা হয়েছে", Toast.LENGTH_SHORT).show()
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text("Clear Demo Data", color = StatusRedDue)
                    }
                }
            }
        }
    }
}
""",

    # 21. PdfReceiptGenerator.kt
    "app/src/main/java/com/chandarkhata/app/util/PdfReceiptGenerator.kt": """package com.chandarkhata.app.util

import android.content.Context
import android.content.Intent
import android.graphics.*
import android.graphics.pdf.PdfDocument
import androidx.core.content.FileProvider
import com.chandarkhata.app.data.dao.BillWithDonorAndPayments
import com.chandarkhata.app.data.model.Committee
import java.io.File
import java.io.FileOutputStream

object PdfReceiptGenerator {
    fun generateAndSharePdf(context: Context, detail: BillWithDonorAndPayments, committee: Committee) {
        val doc = PdfDocument()
        val pageInfo = PdfDocument.PageInfo.Builder(595, 842, 1).create()
        val page = doc.startPage(pageInfo)
        val canvas: Canvas = page.canvas
        val paint = Paint().apply { isAntiAlias = true }

        paint.color = Color.rgb(74, 20, 140)
        canvas.drawRect(0f, 0f, 595f, 110f, paint)

        paint.color = Color.WHITE
        paint.textSize = 20f
        paint.isFakeBoldText = true
        canvas.drawText(committee.bengaliName, 30f, 45f, paint)

        paint.textSize = 13f
        paint.isFakeBoldText = false
        canvas.drawText(committee.name, 30f, 70f, paint)

        paint.color = Color.BLACK
        paint.textSize = 14f
        paint.isFakeBoldText = true
        canvas.drawText("রসিদ নং: \${detail.bill.billNumber}", 30f, 150f, paint)
        canvas.drawText("দাতার নাম: \${detail.donor.fullName}", 30f, 180f, paint)
        canvas.drawText("ঠিকানা: \${detail.donor.address}", 30f, 205f, paint)
        canvas.drawText("ধার্য চাঁদা: ₹ \${detail.bill.billAmount}", 30f, 240f, paint)
        canvas.drawText("মোট আদায়: ₹ \${detail.bill.totalReceived}", 30f, 265f, paint)
        canvas.drawText("বাকি: ₹ \${detail.bill.balanceDue}", 30f, 290f, paint)

        doc.finishPage(page)

        val dir = File(context.cacheDir, "receipts").apply { if (!exists()) mkdirs() }
        val file = File(dir, "\${detail.bill.billNumber}.pdf")
        doc.writeTo(FileOutputStream(file))
        doc.close()

        val uri = FileProvider.getUriForFile(context, "com.chandarkhata.app.fileprovider", file)
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "application/pdf"
            putExtra(Intent.EXTRA_STREAM, uri)
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        }
        context.startActivity(Intent.createChooser(intent, "Share Receipt"))
    }
}
""",

    # 22. DemoDataGenerator.kt
    "app/src/main/java/com/chandarkhata/app/util/DemoDataGenerator.kt": """package com.chandarkhata.app.util

import com.chandarkhata.app.data.dao.ChandarKhataDao
import com.chandarkhata.app.data.model.*

object DemoDataGenerator {
    suspend fun populateDemoData(dao: ChandarKhataDao) {
        val eventId = dao.insertEvent(Event(name = "Durga Puja", year = 2026, budget = 450000.0, isCurrent = true))
        dao.setCurrentEvent(eventId)

        val d1 = dao.insertDonor(Donor(fullName = "Amit Das", address = "12/A Southern Avenue", contactNumber = "9830111222", whatsappNumber = "9830111222", isDemo = true))
        val d2 = dao.insertDonor(Donor(fullName = "Banerjee Sweets", address = "54 Rashbehari Market", contactNumber = "9830222333", whatsappNumber = "9830222333", category = DonorCategory.SHOP_BUSINESS, isDemo = true))

        val b1 = dao.insertBill(DonationBill(billNumber = "CK-2026-0001", donorId = d1, eventId = eventId, billAmount = 2000.0, totalReceived = 2000.0, balanceDue = 0.0, paymentStatus = PaymentStatus.PAID, isDemo = true))
        dao.insertPayment(DonationPayment(billId = b1, amount = 2000.0, paymentMethod = PaymentMethod.CASH, cashAmount = 2000.0, collectorName = "Subhasish", isDemo = true))

        dao.insertBill(DonationBill(billNumber = "CK-2026-0002", donorId = d2, eventId = eventId, billAmount = 5000.0, totalReceived = 0.0, balanceDue = 5000.0, paymentStatus = PaymentStatus.UNPAID, isDemo = true))
    }
}
""",

    # 23. MainActivity.kt
    "app/src/main/java/com/chandarkhata/app/MainActivity.kt": """package com.chandarkhata.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.navigation.NavType
import androidx.navigation.compose.*
import androidx.navigation.navArgument
import com.chandarkhata.app.ui.navigation.Screen
import com.chandarkhata.app.ui.screens.*
import com.chandarkhata.app.ui.theme.ChandarKhataTheme
import com.chandarkhata.app.ui.theme.PurplePrimary
import com.chandarkhata.app.ui.viewmodel.KhataViewModel

class MainActivity : ComponentActivity() {
    private val viewModel: KhataViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            ChandarKhataTheme {
                MainAppHost(viewModel = viewModel)
            }
        }
    }
}

@Composable
fun MainAppHost(viewModel: KhataViewModel) {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route

    val bottomNavItems = listOf(
        Screen.Dashboard to Icons.Default.Dashboard,
        Screen.NewEntry to Icons.Default.AddCircle,
        Screen.PendingDues to Icons.Default.PendingActions,
        Screen.Donors to Icons.Default.People,
        Screen.Settings to Icons.Default.Settings
    )

    Scaffold(
        bottomBar = {
            NavigationBar(containerColor = Color.White) {
                bottomNavItems.forEach { (screen, icon) ->
                    NavigationBarItem(
                        icon = { Icon(icon, screen.titleEnglish) },
                        label = { Text(screen.titleBengali) },
                        selected = currentRoute == screen.route,
                        colors = NavigationBarItemDefaults.colors(selectedIconColor = PurplePrimary, indicatorColor = Color(0xFFF3E5F5)),
                        onClick = {
                            if (currentRoute != screen.route) {
                                navController.navigate(screen.route) { popUpTo("dashboard"); launchSingleTop = true }
                            }
                        }
                    )
                }
            }
        }
    ) { innerPadding ->
        NavHost(navController = navController, startDestination = Screen.Dashboard.route, modifier = Modifier.padding(innerPadding)) {
            composable(Screen.Dashboard.route) {
                DashboardScreen(
                    viewModel = viewModel,
                    onNavigateToNewEntry = { navController.navigate(Screen.NewEntry.route) },
                    onNavigateToPendingDues = { navController.navigate(Screen.PendingDues.route) },
                    onBillClick = { billId -> navController.navigate(Screen.BillDetail.createRoute(billId)) }
                )
            }
            composable(Screen.NewEntry.route) {
                NewEntryScreen(
                    viewModel = viewModel,
                    onBillCreated = { billId -> navController.navigate(Screen.BillDetail.createRoute(billId)) { popUpTo(Screen.Dashboard.route) } },
                    onBack = { navController.popBackStack() }
                )
            }
            composable(Screen.PendingDues.route) {
                PendingDuesScreen(
                    viewModel = viewModel,
                    onOpenBill = { billId -> navController.navigate(Screen.BillDetail.createRoute(billId)) },
                    onBack = { navController.popBackStack() }
                )
            }
            composable(Screen.Donors.route) { DonorsScreen(viewModel = viewModel) }
            composable(Screen.Settings.route) { SettingsScreen(viewModel = viewModel) }
            composable(
                route = Screen.BillDetail.route,
                arguments = listOf(navArgument("billId") { type = NavType.LongType })
            ) { backStack ->
                val billId = backStack.arguments?.getLong("billId") ?: 0L
                BillDetailScreen(billId = billId, viewModel = viewModel, onBack = { navController.popBackStack() })
            }
        }
    }
}
"""
}

print(f"Creating project '{ROOT}'...")
for relative_path, content in FILES.items():
    full_path = os.path.join(ROOT, relative_path.replace("/", os.sep))
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"  [+] Created: {relative_path}")

# Zip the entire project
zip_name = "ChandarKhata.zip"
print(f"\nCompressing into {zip_name}...")
with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(ROOT):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, ".")
            zipf.write(full_path, arcname)

print("\nSUCCESS!")
print(f"1. Your project folder '{ROOT}' has been generated.")
print(f"2. Your ready-to-upload archive '{zip_name}' is created.")