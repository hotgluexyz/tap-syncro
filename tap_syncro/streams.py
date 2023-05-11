"""Stream type classes for tap-syncro."""

from __future__ import annotations

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_syncro.client import syncroStream


class ContactsStream(syncroStream):
    name = "contacts"
    path = "/contacts"
    records_jsonpath = '$.contacts[*]'
    properties = [
        th.Property("id",th.IntegerType),
        th.Property("name",th.StringType),
        th.Property("address1",th.StringType),
        th.Property("address2",th.StringType),
        th.Property("city",th.StringType),
        th.Property("state",th.StringType),
        th.Property("zip",th.StringType),
        th.Property("email",th.StringType),
        th.Property("phone",th.StringType),
        th.Property("mobile",th.StringType),
        th.Property("latitude",th.NumberType),
        th.Property("longitude",th.NumberType),
        th.Property("customer_id",th.IntegerType),
        th.Property("account_id",th.IntegerType),
        th.Property("notes",th.StringType),
        th.Property("created_at",th.DateTimeType),
        th.Property("updated_at",th.DateTimeType),
        th.Property("vendor_id",th.IntegerType),
        th.Property("opt_out",th.BooleanType),
        th.Property("extension",th.StringType),
        th.Property('processed_phone',th.StringType),
        th.Property('processed_mobile',th.StringType),
        th.Property('ticket_matching_emails',th.StringType),
        th.Property("properties", th.CustomType({"type": ["object"]})),
    ]

    schema = th.PropertiesList(*properties).to_dict()


class CustomersStream(syncroStream):
    name="customers"
    path="/customers"
    records_jsonpath="$.customers[*]"
    properties = [
        th.Property("id",th.IntegerType),
        th.Property("firstname",th.StringType),
        th.Property("lastname",th.StringType),
        th.Property("fullname",th.StringType),
        th.Property("business_name",th.StringType),
        th.Property("email",th.StringType),
        th.Property("phone",th.StringType),
        th.Property("mobile",th.StringType),
        th.Property("created_at",th.DateTimeType),
        th.Property("updated_at",th.DateTimeType),
        th.Property("pdf_url",th.StringType),
        th.Property("address",th.StringType),
        th.Property("address_2",th.StringType),
        th.Property("city",th.StringType),
        th.Property("state",th.StringType),
        th.Property("zip",th.StringType),
        th.Property("latitude",th.NumberType),
        th.Property("longitude",th.NumberType),
        th.Property("notes",th.StringType),
        th.Property("get_sms",th.BooleanType),
        th.Property("opt_out",th.BooleanType),
        th.Property("disabled",th.BooleanType),
        th.Property("no_email",th.BooleanType),
        th.Property("location_name",th.StringType),
        th.Property("location_id",th.IntegerType),
        th.Property("online_profile_url",th.StringType),
        th.Property("tax_rate_id",th.IntegerType),
        th.Property("notification_email",th.StringType),
        th.Property("invoice_cc_emails",th.StringType),
        th.Property("invoice_term_id",th.NumberType),
        th.Property("referred_by",th.StringType),
        th.Property("ref_customer_id",th.IntegerType),
        th.Property("business_and_full_name",th.StringType),
        th.Property("business_then_name",th.StringType),
        th.Property( 
            'contacts',
            th.ArrayType( 
                th.ObjectType(*ContactsStream.properties)
            )
        ),
        th.Property("properties",th.CustomType({"type": ["object"]})),
    ]
    schema = th.PropertiesList( 
        *properties
    ).to_dict()

class AppointmentsStream(syncroStream):
    name = "appointments"
    path = "/appointments"
    records_jsonpath = "$.appointments[*]"
    primary_keys=["id"]

    schema = th.PropertiesList(
        th.Property('id',th.IntegerType),
        th.Property('summary',th.StringType),
        th.Property('description',th.StringType),
        th.Property('customer_id',th.IntegerType),
        th.Property('created_at',th.DateTimeType),
        th.Property('updated_at',th.DateTimeType),
        th.Property('start_at',th.DateTimeType),
        th.Property('end_at',th.DateTimeType),
        th.Property('duration',th.NumberType),
        th.Property('location',th.StringType),
        th.Property('ticket_id',th.IntegerType),
        th.Property('appointment_location_type',th.StringType),
        th.Property('start_at_label',th.StringType),
        th.Property('all_day',th.BooleanType),
        th.Property(
            'ticket',
            th.ObjectType(
                th.Property('id',th.IntegerType),
                th.Property('number',th.NumberType),
                th.Property('subject',th.StringType),
                th.Property('created_at',th.StringType),
                th.Property('customer_id',th.IntegerType),
                th.Property('customer_business_then_name',th.StringType),
                th.Property('due_date',th.DateTimeType),
                th.Property('resolved_at',th.DateTimeType),
                th.Property('start_at',th.DateTimeType),
                th.Property('end_at',th.DateTimeType),
                th.Property('location_id',th.IntegerType),
                th.Property('problem_type',th.StringType),
                th.Property('status',th.StringType),
                th.Property('ticket_type_id',th.IntegerType), # TODO: ask about properties
                th.Property('user_id',th.IntegerType),
                th.Property('updated_at',th.DateTimeType),
                th.Property('pdf_url',th.StringType),
                th.Property('priority',th.StringType),
                th.Property('properties',th.CustomType({"type": ["object"]})),
                th.Property(
                    'comments',
                    th.ArrayType(
                        th.ObjectType( 
                            th.Property('id',th.IntegerType),
                            th.Property('created_at',th.DateTimeType),
                            th.Property('updated_at',th.DateTimeType),
                            th.Property('ticket_id',th.IntegerType),
                            th.Property('subject',th.StringType),
                            th.Property('body',th.StringType),
                            th.Property('tech',th.StringType),
                            th.Property('hidden',th.BooleanType),
                            th.Property('user_id',th.IntegerType)
                        )
                    )
                ),
                th.Property(
                    'user',
                    th.ObjectType(
                        th.Property('id',th.IntegerType),
                        th.Property('email',th.StringType),
                        th.Property('full_name',th.StringType),
                        th.Property('created_at',th.StringType),
                        th.Property('updated_at',th.StringType),
                        th.Property('group',th.StringType),
                        th.Property('admin?',th.BooleanType),
                        th.Property('color',th.StringType)
                    )
                ),
            ),
            
        ),
        th.Property(
                'customer',
                th.ObjectType(
                    *CustomersStream.properties
                )
        ),
        th.Property("do_not_email",th.BooleanType)
    ).to_dict()

class AssetsStream(syncroStream):
    name = "assets"
    path="/customer_assets"
    records_jsonpath="$.assets[*]"

    schema = th.PropertiesList( 
        th.Property('id',th.IntegerType),
        th.Property('name',th.StringType),
        th.Property('customer_id',th.IntegerType),
        th.Property('contact_id',th.IntegerType),
        th.Property('created_at',th.DateTimeType),
        th.Property('updated_at',th.DateTimeType),
        th.Property("properties",th.CustomType({"type": ["object"]})),
        th.Property("asset_type",th.StringType),
        th.Property("asset_serial",th.StringType),
        th.Property("external_rmm_link",th.StringType),
        th.Property(
            "rmm_links",
            th.ArrayType(
                th.ObjectType(
                    th.Property('internal_link',th.StringType),
                    th.Property('teamviewer_link',th.StringType),
                    th.Property('screenconnect_link',th.StringType),
                    th.Property('splashtop_link',th.StringType)
                )
            )
        ),
        th.Property('has_live_chat',th.BooleanType),
        th.Property('snmp_enabled',th.BooleanType),
        th.Property('device_info',th.CustomType({"type": ["object"]})),
        th.Property(
            "rmm_store",
            th.ObjectType(
                th.Property("id",th.IntegerType),
                th.Property("asset_id",th.IntegerType),
                th.Property("account_id",th.IntegerType),
                th.Property(
                    "triggers",
                    th.ObjectType(
                        th.Property("bsod_triggered",th.BooleanType),
                        th.Property("time_triggered",th.BooleanType),
                        th.Property("no_av_triggered",th.BooleanType),
                        th.Property("defrag_triggered",th.BooleanType),
                        th.Property("firewall_triggered",th.BooleanType),
                        th.Property("app_crash_triggered",th.BooleanType),
                        th.Property("low_hd_space_triggered",th.BooleanType),
                        th.Property("smart_failure_triggered",th.BooleanType),
                        th.Property("device_manager_triggered",th.BooleanType),
                        th.Property("agent_offline_triggered",th.BooleanType)
                    )
                ),
                th.Property(
                    'windows_updates',
                    th.ObjectType(
                        th.Property(
                            'wu_schedule',
                            th.ObjectType(
                                th.Property('day',th.IntegerType),
                                th.Property('hour',th.IntegerType),
                                th.Property('active_start',th.IntegerType),
                                th.Property('active_end',th.IntegerType)
                            ),
                        ),
                        th.Property('wu_available',th.CustomType({"type": ["object", "string"]})),
                        th.Property('wu_latest',th.CustomType({"type": ["object", "string"]})),
                        th.Property('wu_on',th.CustomType({"type": ["object", "string"]})),
                        th.Property('wu_error',th.CustomType({"type": ["object", "string"]})),
                        th.Property('windows_update',th.CustomType({"type": ["object", "string"]})),
                    )
                ),
                th.Property(
                    'emsisoft',
                    th.ObjectType(
                        th.Property('id',th.IntegerType),
                        th.Property('device_id',th.IntegerType),
                        th.Property(
                            'device_mav_state',
                            th.ObjectType( 
                                th.Property('running',th.BooleanType),
                                th.Property('installed',th.BooleanType),
                                th.Property('def_version',th.BooleanType),
                                th.Property('install_state',th.StringType),
                                th.Property('engine_version',th.StringType),
                                th.Property('last_scan_time',th.DateTimeType),
                                th.Property('product_version',th.StringType),
                                th.Property('product_directory',th.StringType),
                                th.Property('license_expires_at',th.DateTimeType),
                                th.Property('real_time_protection',th.BooleanType),
                                th.Property('anti_phishing',th.BooleanType),
                            )
                        ),
                        th.Property('real_time_protection',th.BooleanType),
                        th.Property('scan',th.BooleanType),
                        th.Property('license',th.StringType),
                        th.Property('own_license',th.StringType),
                        th.Property('own_license_expires_at',th.DateTimeType),
                        th.Property(
                            'email_notifications',
                            th.ObjectType(
                                th.Property('ap_disabled',th.BooleanType),
                                th.Property('rtp_disabled',th.BooleanType),
                                th.Property('last_scan_since',th.BooleanType),
                                th.Property('threats_detected',th.BooleanType),
                            )
                        ),
                        th.Property('scan_schedule',th.StringType),
                        th.Property('anti_phishing',th.BooleanType),
                        th.Property('running',th.BooleanType),
                        th.Property('enabled',th.BooleanType),
                        th.Property('eam_settings',th.ArrayType(th.IntegerType)),
                        th.Property(
                            'scan_opts',
                            th.ObjectType( 
                                th.Property('silent',th.BooleanType),
                                th.Property('scan_type',th.IntegerType),
                                th.Property('quarantine',th.BooleanType),
                            )
                        ),
                        th.Property(
                            'schedule_opts',
                            th.ObjectType( 
                                th.Property('silent',th.BooleanType),
                                th.Property('scan_type',th.IntegerType),
                                th.Property('quarantine',th.BooleanType),
                            )
                        ),
                        th.Property('installed_at',th.DateTimeType)
                    )
                ),
                th.Property('general',th.CustomType({"type": ["object"]})),
                th.Property("created_at",th.DateTimeType),
                th.Property("updated_at",th.DateTimeType),
                th.Property("override_alert_agent_offline_mins",th.NumberType),
                th.Property("override_alert_agent_rearm_after_mins",th.NumberType),
                th.Property("override_low_hd_thresholds",th.CustomType({"type": ["array", "object", "string"]})),
                th.Property("override_low_hd_threshold",th.CustomType({"type": ["array", "object", "string", "number"]})),
                th.Property("override_autoresolve_offline_alert",th.CustomType({"type": ["array", "object", "string"]})),

            )
        ),
        th.Property(
            "address",
            th.ObjectType( 
                th.Property("id",th.IntegerType),
                th.Property("name",th.StringType),
                th.Property("customer_id",th.IntegerType),
                th.Property("address_type_id",th.IntegerType),
                th.Property("address1",th.StringType),
                th.Property("address2",th.StringType),
                th.Property("city",th.StringType),
                th.Property("state",th.StringType),
                th.Property("zip",th.StringType),
                th.Property("latitude",th.NumberType),
                th.Property("longitude",th.NumberType),
                th.Property("created_at",th.DateTimeType),
                th.Property("updated_at",th.DateTimeType),
                th.Property("account_id",th.IntegerType),
            )
        ),
        th.Property( 
            "customer",
            th.ObjectType(*CustomersStream.properties)  
        )
    ).to_dict()



class ContractsStream(syncroStream):
    name= "contracts"
    path="/contracts"
    records_jsonpath = "$.contracts[*]"

    schema = th.PropertiesList( 
        th.Property("id",th.IntegerType),
        th.Property("account_id",th.IntegerType),
        th.Property("customer_id",th.IntegerType),
        th.Property("name",th.StringType),
        th.Property("contract_amount",th.StringType),
        th.Property("start_date",th.DateTimeType),
        th.Property("end_date",th.DateTimeType),
        th.Property("description",th.StringType),
        th.Property("created_at",th.DateTimeType),
        th.Property("updated_at",th.DateTimeType),
        th.Property("status",th.StringType),
        th.Property("likelihood",th.NumberType),
        th.Property("apply_to_all",th.BooleanType),
        th.Property("primary_contact",th.BooleanType),
        th.Property("sla_id",th.IntegerType)
    ).to_dict()


class EstimatesStream(syncroStream):
    name="estimates"
    path="/estimates"
    records_jsonpath="$.estimates[*]"
    primary_keys = ["id"]

    schema = th.PropertiesList(
        th.Property("id",th.IntegerType),
        th.Property("customer_business_then_name",th.StringType),
        th.Property("number",th.StringType),
        th.Property("status",th.StringType),
        th.Property("created_at",th.DateTimeType),
        th.Property("updated_at",th.DateTimeType),
        th.Property('customer_id',th.IntegerType),
        th.Property("date",th.DateTimeType),
        th.Property("subtotal",th.StringType),
        th.Property("total",th.StringType),
        th.Property("tax",th.StringType),
        th.Property("ticket_id",th.IntegerType),
        th.Property("ticket_id",th.IntegerType),
        th.Property("pdf_url",th.StringType),
        th.Property("location_id",th.IntegerType),
        th.Property("invoice_id",th.IntegerType),
        th.Property("employee",th.StringType)
    ).to_dict()
    

class ItemsStream(syncroStream):
    name="items"
    path="/items"
    records_jsonpath="$.items[*]"
    primary_keys = ["id"]

    schema = th.PropertiesList(
        th.Property("id",th.IntegerType),
        th.Property("requestedon",th.DateTimeType),
        th.Property("ticket_num",th.StringType),
        th.Property("parturl",th.StringType),
        th.Property("shipping",th.StringType),
        th.Property("deststore",th.StringType),
        th.Property("orderedby",th.StringType),
        th.Property("orderedon",th.DateTimeType),
        th.Property("trackingnum",th.StringType),
        th.Property('ticketnum',th.IntegerType),
        th.Property("receivedon",th.DateTimeType),
        th.Property("price",th.StringType),
        th.Property('description',th.StringType),
        th.Property("account_id",th.IntegerType),
        th.Property("destination_location_id",th.IntegerType),
        th.Property("from_location_id",th.IntegerType),
        th.Property("from_name",th.StringType),
        th.Property("received_at",th.StringType),
        th.Property("user_id",th.IntegerType),
        th.Property("created_at",th.DateTimeType),
        th.Property("updated_at",th.DateTimeType),
        th.Property("due_at",th.DateTimeType),
        th.Property("ticket_id",th.IntegerType),
        th.Property("logistic_state",th.StringType),
        th.Property("product_id",th.IntegerType),
        th.Property("quantity",th.IntegerType),
        th.Property("round_trip",th.BooleanType),
        th.Property("trip_leg",th.StringType),
        th.Property("retail_cents",th.NumberType),
        th.Property("taxable",th.BooleanType),
        th.Property("converted",th.BooleanType),
        th.Property("notes",th.StringType),
        th.Property("refurb_id",th.IntegerType),
        th.Property("invoice_id",th.IntegerType)
    ).to_dict()
    

class LeadsStream(syncroStream):   
    name="leads"
    path="/leads"
    records_jsonpath="$.customers[*]"
    primary_keys = ["id"]

    schema = th.PropertiesList(
        th.Property("id",th.IntegerType),
        th.Property("first_name",th.StringType),
        th.Property("last_name",th.StringType),
        th.Property("email",th.StringType),
        th.Property("phone",th.StringType),
        th.Property("mobile",th.StringType),
        th.Property("created_at",th.DateTimeType),
        th.Property("updated_at",th.DateTimeType),
        th.Property("address",th.StringType),
        th.Property("city",th.StringType),
        th.Property("state",th.StringType),
        th.Property("zip",th.StringType),
        th.Property("ticket_subject",th.StringType),
        th.Property("ticket_description",th.StringType),
        th.Property("ticket_problem_type",th.StringType),
        th.Property("ticket_id",th.IntegerType),
        th.Property("customer_id",th.IntegerType),
        th.Property("contact_id",th.IntegerType),
        th.Property("mailbox_id",th.IntegerType),
        th.Property("mailbox_name",th.StringType),
        th.Property("business_then_name",th.IntegerType),
        th.Property("has_attachments",th.BooleanType),
        th.Property("message_read",th.BooleanType),
        th.Property("status",th.StringType),
        th.Property("user_id",th.IntegerType),
        th.Property("location_id",th.IntegerType),
    ).to_dict()
     

class PortalUsersStream(syncroStream):
    name="portal_users"
    path="/portal_users"
    records_jsonpath="$.portal_users[*]"
    primary_keys = ["id"]

    schema = th.PropertiesList( 
        th.Property('account_id',th.IntegerType),
        th.Property('portal_group_id',th.IntegerType),
        th.Property("id",th.IntegerType),
        th.Property("email",th.StringType),
        th.Property('disabled',th.BooleanType),
        th.Property("customer_id",th.IntegerType),
        th.Property('contact_id',th.IntegerType),
        th.Property("created_at",th.DateTimeType),
        th.Property("updated_at",th.DateTimeType),
        th.Property('second_factor_attempts_count',th.IntegerType),
        th.Property('encrypted_otp_secret_key',th.StringType),
        th.Property('otp_recovery_secret_key',th.StringType),
        th.Property('encrypted_otp_secret_key_iv',th.StringType),
        th.Property('encrypted_otp_secret_key_salt',th.StringType),
        th.Property('direct_otp',th.StringType),
        th.Property('direct_otp_sent_at',th.DateTimeType),
        th.Property('totp_timestamp',th.DateTimeType),
        th.Property('mobile',th.StringType),
        th.Property('confirmed_mobile',th.StringType),
        th.Property('second_factor_recovery_attempts_count',th.IntegerType),
        th.Property('require_mfa',th.BooleanType)
    ).to_dict()
    

class ProductsStream(syncroStream):
    name="products"
    path="/products"
    records_jsonpath="$.products[*]"
    primary_keys = ["id"]

    schema = th.PropertiesList(
        th.Property("id",th.IntegerType),
        th.Property("price_cost",th.NumberType),
        th.Property("price_retail",th.NumberType),
        th.Property("condition",th.StringType),
        th.Property("description",th.StringType),
        th.Property("maintain_stock",th.BooleanType),
        th.Property("name",th.StringType),
        th.Property("quantity",th.IntegerType),
        th.Property("warranty",th.StringType),
        th.Property("sort_order",th.IntegerType),
        th.Property("reorder_at",th.IntegerType),
        th.Property("disabled",th.BooleanType),
        th.Property("taxable",th.BooleanType),
        th.Property("product_category",th.StringType),
        th.Property("category_path",th.StringType),
        th.Property("upc_code",th.StringType),
        th.Property("discount_percent",th.StringType),
        th.Property("warranty_template_id",th.IntegerType),
        th.Property("qb_item_id",th.IntegerType),
        th.Property("desired_stock_level",th.NumberType),
        th.Property("price_wholesale",th.NumberType),
        th.Property("notes",th.StringType),
        th.Property("tax_rate_id",th.IntegerType),
        th.Property("physical_location",th.StringType),
        th.Property("serialized",th.BooleanType),
        th.Property("vendor_ids",th.ArrayType(th.IntegerType)), ## TODO: Verify
        th.Property("long_description",th.StringType),
        th.Property(
            "location_quantities",
            th.ArrayType(
                th.ObjectType(
                    th.Property('id',th.IntegerType),
                    th.Property('product_id',th.IntegerType),
                    th.Property('location_id',th.IntegerType),
                    th.Property('quantity',th.IntegerType),
                    th.Property('tax_rate_id',th.IntegerType),
                    th.Property('created_at',th.DateTimeType),
                    th.Property('updated_at',th.DateTimeType),
                    th.Property('reorder_at',th.IntegerType),
                    th.Property('desired_stock_level',th.NumberType),
                    th.Property('price_cost_cents',th.NumberType),
                    th.Property('price_retail_cents',th.NumberType),
                )
            )
        ),
        th.Property(
            "photos",
            th.ArrayType(
                th.ObjectType(
                th.Property("id",th.IntegerType),
                th.Property('created_at',th.DateTimeType),
                th.Property('updated_at',th.DateTimeType),
                th.Property('photo_url',th.StringType),
                th.Property('thumbnail_url',th.StringType)
                )
            )
        )
    ).to_dict()

class PurchaseOrdersStream(syncroStream):
    name="purchase_orders"
    path="/purchase_orders"
    records_jsonpath="$.purchase_orders[*]"
    primary_keys = ["id"]

    schema = th.PropertiesList(
        th.Property("id",th.IntegerType),
        th.Property("account_subdomain",th.StringType),
        th.Property("created_at",th.DateTimeType),
        th.Property("updated_at",th.DateTimeType),
        th.Property("expected_date",th.DateTimeType),
        th.Property("number",th.StringType),
        th.Property("other",th.NumberType),
        th.Property("shipping",th.NumberType),
        th.Property("shipping_notes",th.StringType),
        th.Property("status",th.StringType),
        th.Property("total",th.NumberType),
        th.Property("user_id",th.IntegerType),
        th.Property("vendor_id",th.IntegerType),
        th.Property("location_id",th.IntegerType),
        th.Property("due_date",th.DateTimeType),
        th.Property("paid_date",th.DateTimeType),
        th.Property("delivery_tracking",th.StringType),
        th.Property(
            "vendor",
            th.ObjectType(
                th.Property("id",th.IntegerType),
                th.Property("name",th.StringType),
                th.Property("rep_first_name",th.StringType),
                th.Property("rep_last_name",th.StringType),
                th.Property("email",th.StringType),
                th.Property("phone",th.StringType),
                th.Property("account_number",th.StringType),
                th.Property("created_at",th.DateTimeType),
                th.Property("updated_at",th.DateTimeType),
                th.Property("address",th.StringType),
                th.Property("city",th.StringType),
                th.Property("state",th.StringType),
                th.Property("zip",th.StringType),
                th.Property("website",th.StringType),
                th.Property("notes",th.StringType)

            )
        ),
        th.Property("location",th.StringType),
        th.Property(
            "line_items",
            th.ArrayType(
                th.ObjectType( 
                    th.Property("id",th.IntegerType),
                    th.Property("created_at",th.DateTimeType),
                    th.Property("updated_at",th.DateTimeType),
                    th.Property('purchase_order_id',th.IntegerType),
                    th.Property('product_id',th.IntegerType),
                    th.Property('quantity',th.IntegerType),
                    th.Property('cost',th.NumberType),
                    th.Property('total',th.NumberType),
                    th.Property('sku',th.StringType)
                )
            )
        )
    ).to_dict()
     