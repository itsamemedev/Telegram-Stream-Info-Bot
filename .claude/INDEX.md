# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (153)

```
 10467  GET              /                                                dashboard
 14156  GET              /api/abo/status                                  api_abo_status
 10540  GET              /api/active-recordings                           api_active_recordings
 14227  GET              /api/activity-pulse                              api_activity_pulse
 14034  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 20820  GET/POST         /api/audio/config                                api_audio_config
 20850  POST             /api/audio/testtone                              api_audio_testtone
 14100  GET/POST         /api/auto-archive-rules                          api_archive_rules
 14124  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 14128  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 11994  GET              /api/automation/status                           api_automation_status
 12016  POST             /api/automation/toggle                           api_automation_toggle
 13031  GET              /api/azrael/agents                               api_azrael_agents
 11886  POST             /api/azrael/ask                                  api_azrael_ask
 21018  GET/POST         /api/azrael/context                              api_azrael_context
 12736  GET              /api/azrael/core                                 api_azrael_core
 21169  POST             /api/azrael/live_pause                           api_azrael_live_pause
 21159  GET              /api/azrael/live_status                          api_azrael_live_status
 21177  POST             /api/azrael/live_test                            api_azrael_live_test
 13040  GET              /api/azrael/memories                             api_azrael_memories
 21225  POST             /api/azrael/persona                              api_azrael_persona_set
 21216  GET              /api/azrael/personas                             api_azrael_personas
 21253  GET              /api/azrael/piper_status                         api_azrael_piper_status
 20991  POST             /api/azrael/react                                api_azrael_react
 21027  GET              /api/azrael/reaction                             api_azrael_reaction
 21196  GET              /api/azrael/reactions                            api_azrael_reactions
 21246  GET              /api/azrael/transcript                           api_azrael_transcript
 21131  POST             /api/azrael/tts_test                             api_azrael_tts_test
 21102  GET              /api/azrael/voices                               api_azrael_voices
 21270  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 10839  GET              /api/backoff-watch                               api_backoff_watch
 13515  POST             /api/backup/run                                  api_backup_run
 13481  GET              /api/backup/status                               api_backup_status
 13470  POST             /api/backup/system                               api_backup_system
 14066  GET              /api/bandwidth/live                              api_bandwidth_live
 14019  GET              /api/bookmarks                                   api_bookmarks_list
 11102  GET              /api/brain                                       api_brain
 11039  GET              /api/brain/alarms                                api_brain_alarms
 11024  GET              /api/brain/creator                               api_brain_creator
 11001  GET              /api/brain/graph                                 api_brain_graph
 11062  GET              /api/brain/growth                                api_brain_growth
 10017  GET              /api/brain/health                                api_brain_health
 21714  GET              /api/channel/categories                          api_channel_categories
 21720  POST             /api/channel/set                                 api_channel_set
 21567  GET              /api/channels/status                             api_channels_status
 20464  POST             /api/chat/send                                   api_chat_send
 13235  GET              /api/chat/send_status                            api_chat_send_status
 10521  GET              /api/checks                                      api_checks
 21055  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 21038  GET              /api/clips                                       api_clips
 21084  POST/DELETE      /api/clips/clear                                 api_clips_clear
 20742  GET              /api/cohost                                      api_cohost
 20754  POST             /api/cohost/config                               api_cohost_config
 14535  GET              /api/community/stats                             api_community_stats
 22354  GET              /api/data/export                                 api_data_export
 20668  GET              /api/debug/threads                               api_debug_threads
 23201  GET              /api/defense/attacks                             api_defense_attacks
 23168  GET              /api/defense/crowdsec                            api_defense_crowdsec
 23186  GET              /api/defense/fail2ban                            api_defense_fail2ban
 22892  GET              /api/defense/overview                            api_defense_overview
 13577  POST             /api/discord/announce                            api_discord_announce
 13305  GET              /api/discord/clips_week                          api_discord_clips_week
 13521  GET              /api/discord/community                           api_discord_community
 13263  GET              /api/discord/invite                              api_discord_invite
 12837  GET              /api/discord/overview                            api_discord_overview
 12923  POST             /api/discord/webhook_test                        api_discord_webhook_test
 14048  GET              /api/events                                      api_events
 13352  GET              /api/events/stream                               api_events_stream
 14061  GET              /api/forecast/storage                            api_forecast_storage
 12032  GET              /api/freeai/status                               api_freeai_status
 12779  GET              /api/health                                      api_health
 14079  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 14075  GET              /api/heatmap/recordings                          api_heatmap_recordings
 20791  GET              /api/highlights                                  api_highlights
 20803  POST             /api/highlights/config                           api_highlights_config
 20899  POST             /api/kickmod/config                              api_kickmod_config
 20944  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 20958  GET              /api/kickmod/learned                             api_kickmod_learned
 20985  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 20965  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 21313  POST             /api/kickmod/say                                 api_kickmod_say
 21289  POST             /api/kickmod/start                               api_kickmod_start
 20870  GET              /api/kickmod/status                              api_kickmod_status
 21300  POST             /api/kickmod/stop                                api_kickmod_stop
 10401  POST             /api/login                                       dashboard_login_submit
 14520  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 14489  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 13200  GET              /api/notify/status                               api_notify_status
 13211  POST             /api/notify/test                                 api_notify_test
 10625  GET              /api/outcomes                                    api_outcomes
 22191  POST             /api/overlay/config                              api_overlay_config
 22178  POST             /api/overlay/event                               api_overlay_event
 22083  GET              /api/overlay/state                               api_overlay_state
 10658  GET              /api/profile/<username>                          api_profile
 14245  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 14087  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 14210  GET              /api/proxy/heatmap                               api_proxy_heatmap
 14187  GET              /api/proxy/trend                                 api_proxy_trend
 12487  GET              /api/public/stats                                api_public_stats
 10501  GET              /api/pulse                                       api_pulse
 13655  GET              /api/recording-attempts                          api_recording_attempts
 20399  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 20377  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 20418  POST             /api/restream/<int:rid>/start                    api_restream_start
 20689  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 22045  GET              /api/restream/chatfeed                           api_restream_chatfeed
 20353  POST             /api/restream/create                             api_restream_create
 12612  GET              /api/restream/deck                               api_restream_deck
 11968  GET              /api/restream/health                             api_restream_health
 22067  POST             /api/restream/layout                             api_restream_layout
 20326  GET              /api/restream/list                               api_restream_list
 11937  POST             /api/restream/report                             api_restream_report
 20702  POST             /api/restream/start_all                          api_restream_start_all
 20728  POST             /api/restream/stop_all                           api_restream_stop_all
 12143  GET              /api/restream/testpush                           api_testpush_status
 12168  POST             /api/restream/testpush                           api_testpush_run
 14620  GET              /api/restream/verify                             api_restream_verify
 13283  GET              /api/retention/preview                           api_retention_preview
 13292  POST             /api/retention/run                               api_retention_run
 14004  GET              /api/search                                      api_search
 22939  GET              /api/selftest                                    api_selftest
 20435  GET              /api/shield/stats                                api_shield_stats
 10562  GET              /api/storage                                     api_storage
 10569  POST             /api/storage/cleanup                             api_storage_cleanup
 14141  GET              /api/stream/inspect/<username>                   api_stream_inspect
 11907  GET              /api/stream/timeline                             api_stream_timeline
 12911  GET              /api/stream/transcript                           api_stream_transcript
 10593  GET              /api/summary/preview                             api_summary_preview
 13720  GET              /api/system                                      api_system
 14568  GET              /api/system/check_timing                         api_check_timing
 14683  GET              /api/system/config_drift                         api_config_drift
 12947  GET              /api/system/config_snapshot                      api_system_config_snapshot
 13058  GET              /api/system/preflight                            api_system_preflight
 13184  GET              /api/system/preflight_history                    api_system_preflight_history
 13417  GET              /api/system/resilience                           api_system_resilience
 14039  GET              /api/tags                                        api_tags_list
 10535  GET              /api/top                                         api_top
 10894  GET              /api/trend-7d                                    api_trend_7d
 21116  GET              /api/tts/<fn>                                    api_tts_file
 22219  GET              /api/upload_window                               api_upload_window
 10639  GET              /api/userstats                                   api_userstats
 12535  GET              /api/version                                     api_version
 13693  GET              /archive/<int:eid>/download                      archive_download
 13750  GET              /download/<int:recording_id>                     download
 13633  GET              /health                                          health
 20637  GET              /healthz                                         healthz
 10392  GET              /login                                           dashboard_login_page
 10422  GET              /logout                                          dashboard_logout
 10429  GET              /manifest.webmanifest                            pwa_manifest
 12975  GET              /metrics                                         api_prometheus_metrics
 22028  GET              /overlay                                         overlay_page
 10453  GET              /pwa-icon-<variant>.png                          pwa_icon
 10439  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (206)

```
   176  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   146  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   986  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   726  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   857  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   837  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   875  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   799  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   339  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   350  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   360  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   383  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   390  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   401  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   534  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   632  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1224  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1256  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   323  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   939  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   919  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1092  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1140  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1191  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1050  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   894  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   358  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   622  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   504  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   487  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   479  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   315  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   331  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   666  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   631  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   651  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   538  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    33  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    68  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   103  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   265  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   250  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   173  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
    51  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    58  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   194  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   221  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   181  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
    61  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
    94  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   102  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    42  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   118  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   148  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   133  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    73  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
    95  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   116  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
    63  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   163  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    27  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   182  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   202  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   229  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
    57  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    46  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   204  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    70  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   158  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    33  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   140  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   115  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   179  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    66  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    89  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   213  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   203  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   225  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
    84  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   152  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   130  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    69  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   109  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   159  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
    61  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
    86  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
    96  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    35  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    53  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   206  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
    83  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    49  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    60  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   125  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   120  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   111  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    36  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    75  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   250  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   317  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   345  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   196  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   263  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   498  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    63  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   161  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   144  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   384  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   815  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   897  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   925  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   936  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   802  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   864  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   851  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   832  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   477  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   472  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   520  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   403  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   730  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   494  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   457  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   430  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   704  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   574  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   663  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   569  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   502  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   282  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   747  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   370  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   625  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   780  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   765  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   326  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   564  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   550  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   533  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   590  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   683  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   579  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   306  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   296  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   331  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    48  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    69  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    35  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    85  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   109  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   200  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   195  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   255  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   109  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   256  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    71  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   281  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   213  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   237  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   168  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   133  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   193  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    39  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   219  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   434  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   463  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   383  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   396  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   492  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   369  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   244  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   289  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   313  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   300  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   146  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   258  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   116  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   350  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   405  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   104  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
    83  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   115  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
    96  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   106  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    58  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
    82  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    36  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   446  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   412  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   471  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   451  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   434  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   427  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
    33  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    73  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   104  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    88  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   114  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   135  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   147  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    72  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
    96  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    50  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   182  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
```

## Discord-Slash-Commands (45)

```
 23665  /ai                     
 24124  /ask                    
 23756  /assign_role            
 23802  /ban                    
 24456  /botstats               
 24380  /clearwarns             
 24420  /clip                   
 24405  /clipoftheweek          
 24247  /clips                  
 23717  /create_category        
 23686  /create_channel         
 23745  /create_group           
 23728  /create_role            
 23702  /create_voice           
 24038  /daily                  
 24154  /event                  
 24197  /events                 
 24293  /follow                 
 24277  /help                   
 23791  /kick                   
 24020  /leaderboard            
 24233  /livenow                
 24263  /post_test              
 24094  /profile                
 23826  /purge                  
 24006  /rank                   
 24220  /recstatus              
 23767  /remove_role            
 23679  /restream_status        
 23778  /set_channel_perms      
 23971  /setup_community        
 23989  /setup_targets          
 24319  /stats                  
 23591  /status                 
 24615  /streaminfo             
 24512  /sys_report             
 24488  /sys_unpause            
 23813  /timeout                
 24391  /topstreamers           
 23621  /track                  
 23605  /tracklist              
 24308  /unfollow               
 23654  /untrack                
 24341  /warn                   
 24365  /warnings               
```

## Discord-Events (4)

```
 25099  on_member_join
 25061  on_message
 24702  on_raw_reaction_add
 25134  on_ready
```

## Top-Level-Symbole in bot.py (510 Funktionen, 2 Klassen)

```
  2496-2497   _abo_key
  2517-2535   _abo_probe_dump
 22461-22471  _active_recorder_sync
 17615-17622  _ad_allowlist
 18742-18748  _agent_for
 22473-22491  _ai_calls_total_sync
 18751-18767  _ai_telemetry
 19249-19267  _alert
 25250-25300  _alert_monitor_loop
 25681-25743  _announce_loop
  3438-3441   _anthropic_key
  3448-3450   _anthropic_model
 10145-10148  _arg_int
  2488-2493   _as_dict
 15364-15369  _audio_cfg
 19403-19425  _audio_tap_cmd
 10313-10324  _auth_cookie
 10280-10309  _auth_guard
  1644-1649   _auto_on
 20302-20320  _auto_restream_loop
 26802-26817  _azrael_broadcast_reply
 26702-26724  _azrael_chat_reply
 26685-26699  _azrael_chat_should_reply
 26730-26732  _azrael_gate_cfg
 18772-18786  _azrael_live_state
 21931-21945  _azrael_overlay_state
 19132-19186  _azrael_proactive_loop
 18591-18647  _azrael_reaction_to_chats
 26735-26742  _azrael_reply_all_chats
 26672-26682  _azrael_self_names
 26770-26799  _azrael_send_to
 18789-18810  _azrael_system
 25419-25422  _backup_active
 25500-25513  _backup_loop
 17503-17504  _badwords_path
 25212-25221  _brain_growth_loop
 10970-10997  _brain_growth_snapshot
  2424-2444   _brain_hint_delay
 10962-10964  _brain_history_for
  6529-6557   _brain_notify
 10939-10960  _brain_record
 10966-10968  _brain_stream_recent
 13331-13348  _browser_push
  6573-6660   _build_daily_summary
  2927-3107   _build_native_cmd
 15725-15912  _build_restream_cmd
  3151-3184   _build_ytdlp_cmd
 22413-22420  _cached_probe
  5351-5378   _can_stop_tracking
  1824-1846   _capture_set_cookies
 14304-14307  _cfg_get
 14310-14312  _cfg_set
 21675-21710  _channel_set_all
 14962-14965  _chat_connected
 14968-14984  _chat_disconnected
  8625-8636   _chat_is_forum
 15004-15006  _chat_sanitize
 15008-15017  _chat_src_ok
 14947-14959  _chat_stat
 14987-14990  _chat_stats_snapshot
  3713-3724   _check_ai_alive_sync
  3727-3739   _check_ai_models_sync
 22422-22435  _check_redis_alive_sync
 22437-22457  _check_redis_version_sync
 11569-11612  _classify_pool_anonymity
 11615-11632  _classify_pool_anonymity_bg
   802-806    _claude_chat_sync_metered
 10174-10181  _client_ip
 25775-25802  _clip_prune
 25805-25815  _clip_recfile_for
 26331-26337  _clip_should_velocity
 25856-25938  _clip_to_discord
  3611-3620   _close_ai_session
 26846-26861  _cohost_broadcast
 26828-26832  _cohost_cfg
 26887-26899  _cohost_fire_highlight
 26835-26843  _cohost_gate
 26864-26884  _cohost_highlight
 25987-26021  _community_events_loop
 10793-10795  _conv_messages
  6937-6980   _cookie_alarm_loop
  1896-1900   _cookie_autorefresh_info
  1801-1805   _cookie_header
 13381-13413  _cpu_load_snapshot
  3933-3945   _create_index_safe
 22694-22800  _crowdsec_status
 22640-22691  _crowdsec_via_lapi
 22505-22523  _cscli_bin
 22529-22542  _cscli_path
  6827-6852   _daily_summary_loop
 22560-22577  _darf_journal_lesen
 25224-25247  _db_maintenance_loop
  6796-6824   _db_vacuum_loop
 17638-17662  _detect_foreign_ad
  1382-1393   _diag_path_owner
 19038-19082  _director_finalize
 19849-19856  _director_for
 18987-19035  _director_mark
 26225-26260  _disc_automod_check
 26198-26204  _disc_state_get
 26207-26214  _disc_state_set
 23243-23256  _discord_guild_filesize_bytes
 23442-23451  _discord_invite
 26159-26195  _discord_live_thread
 19189-19201  _discord_notify
 23343-23368  _discord_ops_alert
 26057-26155  _discord_post_user
 23507-25209  _discord_run_once
 23381-23439  _discord_start
 25746-25752  _discord_stop
 23264-23266  _discord_upload_limit_label
 23259-23261  _discord_upload_limit_mb
  6855-6932   _disk_alarm_loop
 28279-28328  _disk_autoclean
 28331-28344  _disk_guard_loop
 28271-28276  _disk_pct
 15321-15323  _drawtext_chain
 13847-13849  _dump_all_threads
 11494-11558  _enrich_proxies_with_geo
  2041-2085   _ensure_cookie_file_netscape
 23454-23504  _ensure_discord_invite
 25952-25984  _ensure_error_channel
  8684-8687   _ensure_notify_topic
 11739-11776  _ensure_proxy_ready
  8638-8665   _ensure_topic
   659-661    _env_int
   664-666    _env_int_range
 26024-26054  _error_channel_loop
 19233-19246  _event_webhook
 14770-14783  _evolution_loop
  5971-6005   _extract_file_payload
  2173-2175   _extract_urls_from_streamurl_node
 22545-22552  _f2b_sudo_hint
 19269-19271  _faster_whisper_available
 17527-17539  _fetch_ldnoobw_de
 11383-11401  _fetch_proxy_list
 19683-19711  _fetch_tiktok_room_id
   735-738    _ff_cmd
 15484-15489  _find_chromium
  3144-3148   _find_external_recorder
  2178-2180   _find_stream_urls
 14355-14380  _fire_webhooks
  7716-7725   _fork_safe
   817-826    _freeai_chat_sync_metered
 22595-22637  _geo_lookup_ips
  3600-3609   _get_ai_session
  7550-7590   _get_live_info
  2714-2721   _get_resolve_semaphore
  7980-8346   _handle_single_tracking
 28097-28099  _hb
 28102-28119  _hb_while
 15022-15024  _highlight_cfg
 15027-15056  _highlight_observe
 15492-15510  _htmlov_screenshot_cmd
 19427-19437  _httpx_proxy
 14388-14400  _in_quiet_hours
 29158-29189  _install_fast_eventloop
 10040-10094  _install_fast_json
 13852-13868  _install_faulthandler
 20545-20554  _intel_ensure_schema
 20592-20627  _intel_index_loop
 20566-20576  _intel_index_one
 20557-20563  _intel_semantic
  5340-5349   _is_authorized
  7881-7887   _is_dead
  2163-2165   _is_hevc
 22580-22586  _is_private_ip
  1546-1553   _is_process_running
  6559-6570   _is_quiet_hours
  1183-1192   _is_upload_window
 10129-10142  _json_error_handler
  6782-6783   _kick_broadcaster_id
 12069-12088  _kick_channel_live
  6694-6736   _kick_follower_count
  6678-6681   _kick_slug
 12562-12593  _kick_user_token
  3982-3985   _kind_from_filename
 14417-14422  _latest_popularity
 17549-17555  _learned_load
 17546-17547  _learned_path
 17557-17565  _learned_save
 20064-20097  _live_react_loop
 19860-20053  _live_react_worker
 18650-18661  _live_transcript_push
 20055-20062  _live_users
 19085-19129  _living_title_loop
 17506-17514  _load_banned_words_file
  1722-1795   _load_cookies_dict
 25425-25497  _local_backup_scan
 10111-10125  _log_5xx
 15920-15932  _looks_like_codec_err
 15915-15917  _looks_like_source_expired
  7797-7827   _loop_fehler
 13872-13881  _loop_heartbeat
 28067-28094  _loop_lag_monitor
 13884-13952  _loop_watchdog_thread
 18530-18544  _loyalty_add
 18521-18527  _loyalty_get
 18547-18555  _loyalty_top
 14554-14556  _manual_donations_total
  7889-7890   _mark_dead
 12240-12256  _marketing_loop
 26749-26767  _maybe_handle_command
 28430-28454  _maybe_hype_clip
  3900-3923   _migrate_columns
 27026-27037  _mod_is_exempt
 27040-27045  _mod_warn_first
 27048-27051  _mod_warn_text
 14810-14818  _modlog
   936-938    _multistream_targets
  7728-7729   _nc_create_subprocess_exec
  7732-7733   _nc_create_subprocess_shell
 12492-12509  _news_loop
 14848-14850  _normalize_ingest
  2355-2372   _note_check_duration
  8678-8681   _notify_topic_name
 18676-18684  _oracle_memories
 18942-18976  _oracle_memorize
 18687-18700  _oracle_persona
 18669-18673  _oracle_recent_text
 15147-15155  _ov_atomic_write
 15135-15141  _ov_bar
 17462-17474  _ov_clip_text
 15144-15145  _ov_oneline
 21995-22024  _overlay_push
 15438-15481  _overlay_render_size
 14909-14913  _overlay_session_reset
 21947-21950  _overlay_src_ok
 17625-17635  _own_invites
 15433-15435  _parse_size
 22808-22888  _parse_ssh_attacks
  7152-7185   _pause_resume_cmd
  1850-1894   _persist_refreshed_cookies
  1688-1720   _pick_checked_pull_proxy
 10210-10223  _pin_auth_value
 10269-10270  _pin_clear_fail
 10249-10252  _pin_locked
 10255-10266  _pin_note_fail
 10226-10246  _pin_ok
 21837-21839  _piper_available
 21802-21824  _piper_list_voices
 21844-21869  _piper_pick_model
 21881-21928  _piper_say
 21795-21799  _piper_voice_roots
 14317-14352  _post_json_threaded
 15412-15430  _probe_video_size
  1574-1591   _proc_is_recorder
 11481-11492  _proxy_geo_cache_put
 11708-11736  _proxy_pool_refresh_loop
  1654-1685   _proxy_report_recording
 13837-13839  _prune_stall_dumps
 12310-12431  _public_stats
 19204-19230  _push_notify
 10371-10373  _pwa_dir
 11452-11467  _quick_validate_proxy
 14383-14385  _quiet_hours_config
 10336-10369  _rate_guard
 18495-18501  _react_warn
  7636-7675   _reap_proc
  2395-2417   _record_check_outcome
   730-732    _redact_stream_urls
 11635-11705  _refresh_proxy_pool
 21827-21833  _resolve_piper_model
  2189-2279   _resolve_via_html
  2537-2691   _resolve_via_webcast_api_v2
  2754-2816   _resolve_via_ytdlp
 26376-26505  _resolve_youtube_ingest
 20136-20143  _restream_active_platforms
 14894-14905  _restream_active_sources
 19714-19813  _restream_chat_guardian
 15059-15131  _restream_chat_push
 14821-14833  _restream_enabled
 15513-15600  _restream_html_overlay_start
 15603-15616  _restream_html_overlay_stop
  1131-1133   _restream_layout_mode
 14859-14882  _restream_overlay_files
 20101-20133  _restream_platform_state
 20264-20299  _restream_resume_after_restart
 15664-15722  _restream_tts_enqueue_wav
 15374-15406  _restream_tts_feeder
 15371-15372  _restream_tts_fifo_path
 15619-15646  _restream_tts_start
 15648-15662  _restream_tts_stop
 20146-20261  _restream_verify_loop
 25390-25402  _retention_loop
 25349-25387  _retention_scan
  2499-2501   _room_is_abo
  6009-6126   _run_ai_call
 13975-13988  _run_async_from_flask
 22589-22592  _run_priv
 29146-29154  _run_selfcheck_and_exit
 25405-25416  _s3_client
  7916-7967   _safe_send
  4604-4620   _sample_net_throughput
 17516-17524  _save_banned_words_file
  2447-2474   _schedule_next_check
 25303-25346  _scheduler_loop
  3926-3930   _schema_pk
 13992-13997  _scraper_session
 27054-27093  _screen_full
 12795-12832  _sec_headers
  2168-2170   _select_stream_from_data_section
 28959-29143  _selfcheck
  8690-8724   _send_live_notice
  1206-1210   _should_defer_upload
 25818-25853  _shrink_for_discord
 10376-10388  _sicheres_ziel
 28351-28368  _sign_health_check
 28371-28390  _sign_health_loop
  7745-7756   _spawn
  7759-7789   _spawn_from_flask
 22932-22935  _st_befund
 19439-19680  _start_chat_listener
 13955-13972  _start_loop_watchdog
 12455-12483  _stats_loop
 12434-12437  _stats_output_path
 12440-12452  _stats_write
  8418-8434   _storage_cleanup_loop
 28410-28417  _story_for
  3206-3212   _stream_url_expiry
  3221-3227   _stream_url_is_fresh
  3214-3219   _stream_url_ttl
 17589-17596  _streamer_persona_get
 17571-17577  _streamer_personas_load
 17568-17569  _streamer_personas_path
 17579-17587  _streamer_personas_save
 15326-15330  _studio_chain
 25522-25644  _system_backup
 25647-25677  _system_backup_loop
 11404-11443  _test_proxy
 12110-12119  _testpush_cfg
 12122-12139  _testpush_exec
 12091-12107  _testpush_resolve_live
  7892-7913   _tg_sprache_setzen
  8597-8607   _tg_topics_load_into_mem
  8594-8595   _tg_topics_path
  8609-8616   _tg_topics_save
 10184-10192  _token_ok
  8619-8623   _topic_forget
 14403-14414  _tracking_max_duration
  4191-4205   _tracking_remove_cleanup
  4222-4234   _tracking_resume_cleanup
  1440-1463   _try_attach_file_handler
 21871-21879  _tts_cleanup
 12047-12051  _tunnel_effective
 21334-21387  _twitch_channel_status
 27096-27239  _twitch_chat_loop
 26910-27013  _twitch_eventsub_loop
  1229-1242   _upload_queue_add
  1253-1255   _upload_queue_count
  1212-1221   _upload_queue_load
  1202-1204   _upload_queue_path
  1244-1251   _upload_queue_remove
  1223-1227   _upload_queue_save
  1257-1298   _upload_window_loop
  7609-7616   _uptime_s
 14836-14845  _url_host
   710-727    _url_ohne_zugang
   795-799    _usage_record_claude
  7830-7874   _verbindung_verloren
  6739-6770   _viewer_sample_loop
  6786-6793   _viewer_stats
 10273-10276  _wants_html
  7619-7633   _warn_empty_env
 28140-28261  _watchdog_loop
 26651-26659  _wchat_thank_ok
 19273-19303  _whisper_get_model
  7706-7713   _whisper_native_section
 18482-18488  _whisper_pool
 19372-19401  _whisper_segments
 19305-19369  _whisper_transcribe
 15157-15319  _write_restream_overlay
 27267-27346  _youtube_api_chat_loop
 21390-21493  _youtube_api_status
 21496-21563  _youtube_channel_status
 27349-27509  _youtube_chat_loop
 26511-26524  _youtube_restream_autoconfig
 26527-26551  _youtube_restream_autoconfig_inner
 26618-26646  _youtube_send
 21631-21672  _youtube_set_channel
 26554-26588  _yt_access_token
 26591-26606  _yt_live_chat_id
 27260-27264  _yt_oauth_configured
 26614-26615  _yt_sendrate_cfg
 27242-27257  _yt_timeout
  2738-2739   _ytdlp_detect_available
  2741-2752   _ytdlp_note_result
 13842-13844  _zombie_child_count
  7486-7510   about
  4101-4105   add_ai_log_entry
  4018-4021   add_archive_entry
  4717-4732   add_archive_rule
  4393-4427   add_recording
  4166-4183   add_tracking
  6129-6162   ai
  3753-3804   ai_chat
  3838-3848   ai_history_append
  3850-3855   ai_history_clear
  3827-3836   ai_history_load
  3812-3825   ai_rate_limit_check
  6191-6199   aireset
 18813-18832  azrael_chat
 27514-27636  brain_cmd
  3230-3414   build_recording_cmd
  4186-4189   bulk_add_trackings
  6983-7042   bulkadd
  8437-8577   check_all_trackings
  4238-4250   claim_live_transition
 17665-18420  class KickModerator
 15935-17349  class RestreamManager
 11821-11863  classify_proxy_anonymity
  6237-6435   cleanup
  5200-5241   cleanup_old_recordings
  4384-4391   clear_recording
 26263-26328  clip_moment
  4548-4597   compute_storage_forecast
  7105-7149   cookies_cmd
  4157-4163   count_trackings_for_chat
  4088-4099   decide_preferred_recorder
  4028-4031   delete_archive_entry
  4734-4742   delete_archive_rule
  5666-5813   diag
 27748-27809  einnahmen_cmd
  4542-4545   find_recordings_by_fingerprint
  4049-4065   finish_recording_attempt
  4210-4212   get_all_active_trackings
  4116-4119   get_all_checks
  4429-4432   get_all_recordings
  4491-4493   get_all_tags_with_counts
  4519-4522   get_annotations_for_recording
  4023-4026   get_archive_entry
  4512-4515   get_bookmarked_recordings
  1917-2034   get_cookie_health
  4479-4485   get_event_log
  4072-4086   get_last_recording_attempt
  2819-2924   get_live_status
  5000-5003   get_manual_recordings
  4527-4530   get_or_compute_inspect_sync
  5276-5320   get_outcome_breakdown
  4498-4501   get_priority_poll_interval
  4695-4704   get_profile_snapshots
  4067-4070   get_recent_recording_attempts
  4434-4437   get_recording_by_id
  4505-4508   get_recording_note
  3548-3571   get_redis
  4146-4149   get_stats
  5167-5198   get_storage_stats
  4835-4837   get_tiktok_status_distribution
  4252-4261   get_tracking_state
  4207-4208   get_trackings_for_group
  5016-5019   get_trash_recordings
  9345-10008  handle_recording_finished
  3948-3973   init_db
  5090-5144   inspect_stream_url
 21990-21992  is_revenue_platform
  4707-4715   list_archive_rules
  5470-5508   live
  7970-7978   live_check_worker
  3623-3657   llm_chat
  3680-3708   llm_chat_sync
  3665-3677   llm_list_models
  4445-4471   log_event
  1508-1541   log_recording_failure
  7299-7348   logs_cmd
 28458-28949  main
  6165-6188   on_ai_media
  7425-7451   on_ai_reply
  7454-7483   on_azrael_mention
  7515-7545   on_callback
 18835-18939  oracle_handle
  7188-7191   pause_tracking
  5330-5335   profile_keyboard
  7250-7296   quota
  8348-8415   reaper_loop
  4831-4833   record_tiktok_status
  6204-6234   recstatus
  3573-3581   redis_get_json
  3583-3589   redis_set_json
 27812-27822  report_cmd
 11866-11868  report_proxy_result
  2282-2309   resolve_tiktok_live_stream
  5011-5014   restore_recording
  7194-7197   resume_tracking
  4745-4825   run_archive_rules
 27825-28047  run_bot
 13764-13811  run_flask
  4623-4668   sample_bandwidth_for_active
  4674-4693   save_profile_snapshot
  4108-4114   save_tiktok_check
  4376-4382   set_recording_file
  4215-4219   set_tracking_paused
  5006-5009   soft_delete_recording
  8730-9343   split_and_send_video
  5383-5425   start
  4033-4047   start_recording_attempt
  6438-6476   stats
  4981-4998   stop_manual_recording
  7200-7247   stoprec
  6663-6671   summary_cmd
  7351-7422   sysres
  5815-5959   teststream
  5427-5468   tiktok
  7045-7102   topusers
  5545-5602   track
  5510-5542   track_exact
  5616-5664   tracklist
  4847-4979   trigger_manual_recording
  4337-4374   try_acquire_recording_lock
  5022-5081   universal_search
  5604-5614   untrack
 27639-27745  update_cmd
  4537-4540   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
binresolve.py          resolve
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, yt_sendrate_cfg
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, live_ping, note_chatter, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_conn, get_pool, set_pool
director.py            class LiveDirector, configure
discordlimits.py       describe, effective_upload_mb, gate_mb, guild_limit_mb
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
highlights.py          check, new_state, observe, score
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             broadcaster_id, configure, oauth_exchange, slug
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
persona.py             —
piper_voices.py        resolve_model_path, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
restrend.py            rising_trend
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             changelog, current, latest, summary_line
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
